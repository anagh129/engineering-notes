"""
Single-file Django + Graphene example: model, query, mutation, and a demo run.

Setup:
    pip install django graphene-django

Run:
    python django_graphene_single_file.py
"""
import django
from django.conf import settings

# ---------------------------------------------------------------------------
# 1. Minimal Django configuration (no project, no manage.py needed)
# ---------------------------------------------------------------------------
settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
    },
    INSTALLED_APPS=["django.contrib.contenttypes"],
    DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
)
django.setup()

import graphene  # noqa: E402
from django.db import connection, models  # noqa: E402
from graphene_django import DjangoObjectType  # noqa: E402


# ---------------------------------------------------------------------------
# 2. Model
# ---------------------------------------------------------------------------
class Milestone(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, default="")
    obsolete = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "demo"  # needed because this file is not a real Django app

    def __str__(self):
        return f"{self.identifier} - {self.name}"


# ---------------------------------------------------------------------------
# 3. GraphQL type
# ---------------------------------------------------------------------------
class MilestoneType(DjangoObjectType):
    class Meta:
        model = Milestone
        fields = ("id", "name", "identifier", "description", "obsolete", "updated_at")


# ---------------------------------------------------------------------------
# 4. Query
# ---------------------------------------------------------------------------
class Query(graphene.ObjectType):
    milestones = graphene.List(
        MilestoneType,
        include_obsolete=graphene.Boolean(default_value=False),
    )
    milestone = graphene.Field(MilestoneType, id=graphene.ID(required=True))

    def resolve_milestones(root, info, include_obsolete):
        qs = Milestone.objects.all().order_by("id")
        if not include_obsolete:
            qs = qs.filter(obsolete=False)
        return qs

    def resolve_milestone(root, info, id):
        return Milestone.objects.filter(pk=id).first()


# ---------------------------------------------------------------------------
# 5. Mutations
# ---------------------------------------------------------------------------
class CreateMilestone(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        identifier = graphene.String(required=True)
        description = graphene.String()

    milestone = graphene.Field(MilestoneType)

    def mutate(root, info, name, identifier, description=""):
        if Milestone.objects.filter(identifier=identifier).exists():
            raise Exception(f"Identifier '{identifier}' already exists")
        milestone = Milestone.objects.create(
            name=name, identifier=identifier, description=description
        )
        return CreateMilestone(milestone=milestone)


class UpdateMilestone(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        obsolete = graphene.Boolean()

    milestone = graphene.Field(MilestoneType)

    def mutate(root, info, id, **kwargs):
        milestone = Milestone.objects.filter(pk=id).first()
        if milestone is None:
            raise Exception("Milestone not found")
        for field, value in kwargs.items():
            setattr(milestone, field, value)
        milestone.save()
        return UpdateMilestone(milestone=milestone)


class DeleteMilestone(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, id):
        deleted, _ = Milestone.objects.filter(pk=id).delete()
        return DeleteMilestone(ok=deleted > 0)


class Mutation(graphene.ObjectType):
    create_milestone = CreateMilestone.Field()
    update_milestone = UpdateMilestone.Field()
    delete_milestone = DeleteMilestone.Field()


# ---------------------------------------------------------------------------
# 6. Schema
# ---------------------------------------------------------------------------
schema = graphene.Schema(query=Query, mutation=Mutation)


# ---------------------------------------------------------------------------
# 7. Demo
# ---------------------------------------------------------------------------
def run(title, query, variables=None):
    result = schema.execute(query, variable_values=variables)
    print(f"\n--- {title} ---")
    if result.errors:
        print("ERRORS:", result.errors)
    else:
        print(result.data)
    return result


if __name__ == "__main__":
    # Create the table directly (no migrations needed for this demo)
    with connection.schema_editor() as editor:
        editor.create_model(Milestone)

    run(
        "Create",
        """
        mutation {
          createMilestone(name: "Design Freeze", identifier: "M-001",
                          description: "Design is locked") {
            milestone { id name identifier obsolete }
          }
        }
        """,
    )

    run(
        "Create (with variables)",
        """
        mutation Create($name: String!, $identifier: String!) {
          createMilestone(name: $name, identifier: $identifier) {
            milestone { id name identifier }
          }
        }
        """,
        {"name": "Release", "identifier": "M-002"},
    )

    run("List", "{ milestones { id name identifier description obsolete } }")

    run("Get by id", '{ milestone(id: 1) { id name identifier description } }')

    run(
        "Update (set obsolete)",
        """
        mutation {
          updateMilestone(id: 1, obsolete: true, description: "No longer used") {
            milestone { id name obsolete description }
          }
        }
        """,
    )

    run("List (active only)", "{ milestones { id name obsolete } }")
    run("List (include obsolete)", "{ milestones(includeObsolete: true) { id name obsolete } }")

    run("Duplicate identifier", """
        mutation { createMilestone(name: "Dup", identifier: "M-002") {
          milestone { id } } }
    """)

    run("Delete", "mutation { deleteMilestone(id: 2) { ok } }")
    run("List after delete", "{ milestones(includeObsolete: true) { id name } }")