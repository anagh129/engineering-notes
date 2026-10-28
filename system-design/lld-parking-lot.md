# Q1: Design a Parking Lot (Interviewee's Walkthrough)

**Interviewer:** "Design a multi-level parking lot that supports different vehicle types (bike, car, truck). It should issue a ticket on entry and calculate the fee on exit. How would you add EV charging spots later?"

**Sources:**
- https://www.designgurus.io/blog/low-level-design-interview
- https://www.educative.io/blog/low-level-design-interview-questions-for-system-design-roles
- https://leetcode.com/discuss/post/5328221/frequently-asked-low-level-design-lld-qu-l0xk/
- https://www.systemdesignhandbook.com/blog/low-level-system-design-interview-questions/
- https://www.techinterview.org/post/3233463532/low-level-design-parking-lot/

---

## Step 1: Clarifying Questions

**Me:** Before I design anything, let me confirm scope. I'll state my assumption for each question so we can move on if you agree.

1. **Vehicle types?** Bike, car and truck. Should the design allow new types later? *I'll assume yes.*
2. **Spot types?** Do spots match vehicle sizes (small, medium, large)? *I'll assume a bike takes a small spot, a car a medium, and a truck a large, and that a smaller vehicle may use a larger spot if its own size is full.*
3. **Multiple floors and entry/exit gates?** *I'll assume multiple floors and multiple gates.*
4. **Pricing?** Hourly by vehicle type? *I'll assume hourly rates that vary by vehicle type, but the pricing rule must be swappable.*
5. **Payment?** Do I model the actual payment gateway or just the amount? *I'll assume I calculate the fee and record a payment, and mock the gateway.*
6. **Concurrency?** Can two cars arrive at the same time? *I'll assume yes, so spot allocation must be thread-safe.*
7. **Out of scope:** reservations, a UI, and a database. I'll keep everything in memory.

---

## Step 2: Functional Requirements

- Park a vehicle: find a free spot, mark it occupied, issue a ticket.
- Unpark a vehicle: take the ticket, calculate the fee, free the spot.
- Show availability per floor and per spot type.
- Support multiple floors, vehicle types and pricing rules.

**Non-functional:** thread-safe allocation, easy to extend (new vehicle type, EV spots, new pricing), and clean separation of responsibilities.

---

## Step 3: Identify Entities

I pull the nouns from the requirements.

| Entity | Responsibility |
|---|---|
| `ParkingLot` | Entry point (facade). Holds floors and coordinates park/unpark. |
| `ParkingFloor` | Holds spots and finds an available spot. |
| `ParkingSpot` | Knows its type, whether it is free, and which vehicle is in it. |
| `Vehicle` | Has a license plate and a type. |
| `Ticket` | Entry time, vehicle, spot, ticket id. |
| `Payment` | Amount, status, time. |
| `SpotAllocationStrategy` | Decides which spot to give. |
| `PricingStrategy` | Decides how the fee is calculated. |

---

## Step 4: Relationships

```
ParkingLot   1 ──── *    ParkingFloor
ParkingFloor 1 ──── *    ParkingSpot
ParkingSpot  1 ──── 0..1 Vehicle   (when occupied)
Ticket       * ──── 1    Vehicle, 1 ParkingSpot
ParkingLot   uses  SpotAllocationStrategy, PricingStrategy
```

I'd use **composition** for the lot, floors and spots, since a spot has no meaning without its floor. I'd use **inheritance only where behavior differs**, and prefer **composition and strategies** elsewhere.

---

## Step 5: Design Patterns I'd Use (and Why)

- **Strategy** for spot allocation (nearest to the entrance, lowest floor first, and so on). It's open for extension without modifying `ParkingLot`.
- **Strategy** for pricing (hourly, flat, peak-hour). The rules change often, so they shouldn't live inside `ParkingLot`.
- **Factory** (optional) to create a vehicle or spot from its type.
- **Singleton** for `ParkingLot`. I'd mention it but be careful. It hurts testability, so I'd prefer dependency injection unless the interviewer wants a singleton.

I'm deliberately *not* using State or Observer here. Nothing in the requirements needs them, and forcing patterns is a red flag.

---

## Step 6: Core Code (Python)

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from threading import Lock
from typing import Optional
import math
import uuid


# ---------- Enums & Exceptions ----------

class VehicleType(Enum):
    BIKE = "BIKE"
    CAR = "CAR"
    TRUCK = "TRUCK"


class SpotType(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class ParkingFullException(Exception):
    pass


class InvalidTicketException(Exception):
    pass


class DuplicateVehicleException(Exception):
    pass


# ---------- Vehicles ----------

class Vehicle:
    def __init__(self, plate: str, vehicle_type: VehicleType):
        self.plate = plate
        self.type = vehicle_type


class Bike(Vehicle):
    def __init__(self, plate: str):
        super().__init__(plate, VehicleType.BIKE)


class Car(Vehicle):
    def __init__(self, plate: str):
        super().__init__(plate, VehicleType.CAR)


class Truck(Vehicle):
    def __init__(self, plate: str):
        super().__init__(plate, VehicleType.TRUCK)


# ---------- Spot & Floor ----------

class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: SpotType):
        self.id = spot_id
        self.type = spot_type
        self._vehicle: Optional[Vehicle] = None
        self._lock = Lock()

    def try_park(self, vehicle: Vehicle) -> bool:
        """Atomic check-and-set: only one thread can take a free spot."""
        with self._lock:
            if self._vehicle is not None:
                return False
            self._vehicle = vehicle
            return True

    def free(self) -> None:
        with self._lock:
            self._vehicle = None

    def is_free(self) -> bool:
        with self._lock:
            return self._vehicle is None


class ParkingFloor:
    def __init__(self, number: int, spots: list[ParkingSpot]):
        self.number = number
        self.spots = spots

    def available_count(self, spot_type: SpotType) -> int:
        return sum(1 for s in self.spots if s.type == spot_type and s.is_free())


# ---------- Ticket ----------

@dataclass
class Ticket:
    vehicle: Vehicle
    spot: ParkingSpot
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entry_time: datetime = field(default_factory=datetime.now)


# ---------- Strategy: Spot Allocation ----------

class SpotAllocationStrategy(ABC):
    @abstractmethod
    def find_spot(self, floors: list[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
        ...


# Preference order: exact fit first, then larger spots as fallback.
COMPATIBLE_SPOTS = {
    VehicleType.BIKE:  [SpotType.SMALL, SpotType.MEDIUM, SpotType.LARGE],
    VehicleType.CAR:   [SpotType.MEDIUM, SpotType.LARGE],
    VehicleType.TRUCK: [SpotType.LARGE],
}


class LowestFloorFirstStrategy(SpotAllocationStrategy):
    def find_spot(self, floors, vehicle):
        for spot_type in COMPATIBLE_SPOTS[vehicle.type]:
            for floor in sorted(floors, key=lambda f: f.number):
                for spot in floor.spots:
                    if spot.type == spot_type and spot.is_free():
                        return spot
        return None


# ---------- Strategy: Pricing ----------

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, ticket: Ticket, exit_time: datetime) -> float:
        ...


class HourlyPricing(PricingStrategy):
    def __init__(self, rate_per_hour: dict[VehicleType, float]):
        self.rate_per_hour = rate_per_hour

    def calculate_fee(self, ticket, exit_time):
        seconds = (exit_time - ticket.entry_time).total_seconds()
        hours = max(1, math.ceil(seconds / 3600))  # minimum 1 hour
        return hours * self.rate_per_hour[ticket.vehicle.type]


# ---------- Facade ----------

class ParkingLot:
    def __init__(self, floors: list[ParkingFloor],
                 allocator: SpotAllocationStrategy,
                 pricing: PricingStrategy):
        self.floors = floors
        self.allocator = allocator
        self.pricing = pricing
        self._active_tickets: dict[str, Ticket] = {}
        self._active_plates: set[str] = set()
        self._state_lock = Lock()  # guards only the dict and set

    def park(self, vehicle: Vehicle) -> Ticket:
        # Reserve the plate atomically so the same vehicle can't park twice.
        with self._state_lock:
            if vehicle.plate in self._active_plates:
                raise DuplicateVehicleException(vehicle.plate)
            self._active_plates.add(vehicle.plate)

        try:
            # Retry loop: another thread may grab the spot between find and park.
            while True:
                spot = self.allocator.find_spot(self.floors, vehicle)
                if spot is None:
                    raise ParkingFullException()
                if spot.try_park(vehicle):
                    ticket = Ticket(vehicle, spot)
                    with self._state_lock:
                        self._active_tickets[ticket.id] = ticket
                    return ticket
        except Exception:
            with self._state_lock:
                self._active_plates.discard(vehicle.plate)
            raise

    def unpark(self, ticket_id: str) -> float:
        with self._state_lock:
            ticket = self._active_tickets.pop(ticket_id, None)
            if ticket is None:
                raise InvalidTicketException(ticket_id)
            self._active_plates.discard(ticket.vehicle.plate)

        fee = self.pricing.calculate_fee(ticket, datetime.now())
        ticket.spot.free()
        return fee


# ---------- Demo ----------

if __name__ == "__main__":
    floors = [
        ParkingFloor(1, [
            ParkingSpot("1-S1", SpotType.SMALL),
            ParkingSpot("1-M1", SpotType.MEDIUM),
            ParkingSpot("1-L1", SpotType.LARGE),
        ]),
    ]
    lot = ParkingLot(
        floors,
        LowestFloorFirstStrategy(),
        HourlyPricing({VehicleType.BIKE: 10, VehicleType.CAR: 40, VehicleType.TRUCK: 80}),
    )

    ticket = lot.park(Car("KA01AB1234"))
    print("Parked at:", ticket.spot.id)
    print("Fee:", lot.unpark(ticket.id))  # 40 (minimum 1 hour)
```

Two points I'd call out:
- `try_park` is an **atomic check-and-set** using a per-spot `Lock`, so two threads can't take the same spot.
- `park()` **retries** if it loses the race. Only the spot is locked, plus a short lock on the ticket dict, not the whole lot, so throughput stays high.

---

## Step 7: Extensibility (Answering the EV Question)

**Interviewer asked:** "How would you add EV charging spots?"

```python
class SpotType(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    EV = "EV"                       # 1. new spot type


class ElectricCar(Vehicle):         # 2. new vehicle type
    def __init__(self, plate: str):
        super().__init__(plate, VehicleType.ELECTRIC_CAR)


class ChargingSpot(ParkingSpot):    # spot with extra behavior
    def __init__(self, spot_id: str):
        super().__init__(spot_id, SpotType.EV)
        self.charging = False

    def start_charging(self): self.charging = True
    def stop_charging(self):  self.charging = False


class EVPricing(PricingStrategy):   # 3. parking fee + charging fee
    def __init__(self, base: PricingStrategy, charge_rate_per_hour: float):
        self.base = base
        self.charge_rate = charge_rate_per_hour

    def calculate_fee(self, ticket, exit_time):
        hours = max(1, math.ceil((exit_time - ticket.entry_time).total_seconds() / 3600))
        return self.base.calculate_fee(ticket, exit_time) + hours * self.charge_rate

# 4. In COMPATIBLE_SPOTS add:
#    VehicleType.ELECTRIC_CAR: [SpotType.EV, SpotType.MEDIUM, SpotType.LARGE]
```

`ParkingLot` itself doesn't change. That is the Open/Closed Principle in practice. (Add `ELECTRIC_CAR = "ELECTRIC_CAR"` to `VehicleType` as well.)

---

## Step 8: Edge Cases I'd Handle

- Lot full, so raise `ParkingFullException` (or return a "full" result for the display board).
- Lost or invalid ticket, so raise `InvalidTicketException`, with a fallback fee policy for lost tickets.
- Same vehicle parked twice, so check by plate (`DuplicateVehicleException`).
- Fee for under one hour: minimum one hour (a pricing-rule decision).
- Spot downgrade or upgrade: a bike in a medium spot when small spots are full.
- Concurrent entry and exit, handled by per-spot locks and a short lock on the ticket state.

---

## Step 9: Trade-offs I'd Mention

- **Floor-level search is O(floors x spots).** For speed I'd keep a `deque` of free spots per spot type per floor, so allocation becomes O(1).
- **Fine-grained locking** (per spot) over a global lock on `ParkingLot`.
- **Python's GIL** doesn't make check-then-act sequences safe, so the explicit `Lock` is still required.
- **In-memory only.** In production the state would be persisted, but that's outside LLD scope.

---

## Open Floor

**Me:** That's my design end to end. I'm happy to go deeper on any of these:

- Drawing the full UML class diagram
- Implementing a `NearestSpotStrategy` or a free-spot `deque`
- Adding a `Payment` flow with multiple methods (cash, card, UPI)
- Entry/exit gate classes and a display board (Observer)
- Handling reservations or a monthly pass
- Unit tests for the concurrency scenario (using `threading`)

What would you like me to dig into, or is there a requirement I should revisit?


# Last: Go through
