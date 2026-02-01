# Clean Architecture Refactoring - Answers

## 1. Why can we not easily split this project into two microservices?

The project has several issues preventing easy microservice separation:

### Tight Coupling Through Shared Database

**Example: Foreign Key Relationships**
```python
# All entities in same database with foreign keys
class CartItem(Base):
    __tablename__ = "cart_items"
    user_id = Column(UUID, ForeignKey("users.id"))  # FK to users table
    item_id = Column(UUID, ForeignKey("items.id"))  # FK to items table
```

If you split into User Service and Item Service:
- CartItem has foreign keys to BOTH tables
- Cannot enforce referential integrity across services
- Need distributed transactions or eventual consistency
- Breaking foreign keys breaks data integrity

**Example: Shared SQLAlchemy Models**
```python
# user/repository.py
from be_task_ca.models import User, Item, CartItem  # Shared models!

def find_cart_items_for_user_id(user_id: UUID):
    # User service accessing Item data directly
    return db.query(CartItem).join(Item).filter(...)
```

Problem: User service directly queries Item table, cannot separate databases.

### No Clear Bounded Contexts

**Example: Mixed Responsibilities**
```python
# user/repository.py - User service doing cart AND item operations
def save_user(email, password):  # User domain
    ...

def find_cart_items_for_user_id(user_id):  # Cart domain
    ...

# item/repository.py - Item service also handling cart
def save_item(name, price):  # Item domain
    ...

def find_item_by_id(item_id):  # Used by cart domain
    ...
```

**What's missing:**
```python
# Should have separate bounded contexts:

# User Service - Identity & Access
- save_user()
- find_user_by_email()
- authenticate_user()

# Catalog Service - Product Information
- save_item()
- list_items()
- find_item_by_id()

# Cart Service - Shopping Cart
- add_to_cart()
- get_user_cart()
- update_cart_item_quantity()
```

### Cross-Domain Business Logic

**Example: Cart Operation Needs Both Domains**
```python
# Original: Everything in one place
def add_to_cart(user_id: UUID, item_id: UUID, quantity: int):
    user = find_user_by_id(user_id)      # User domain
    if not user:
        raise HTTPException(404)

    item = find_item_by_id(item_id)      # Item domain
    if not item:
        raise HTTPException(404)

    if item.quantity < quantity:          # Item business rule
        raise HTTPException(400)

    cart_item = CartItem(...)            # Cart domain
    db.add(cart_item)
```

**Problem:** One operation touches 3 domains, impossible to split

**How it should work with microservices:**
```python
# Cart Service makes API calls to other services
# Important: My new implementation does not implement microservices as well, it only splits into 
# a clean architecture but is still not a microservice.
async def add_to_cart(user_id: UUID, item_id: UUID, quantity: int):
    # Call User Service API
    user = await user_service_client.get_user(user_id)
    if not user:
        raise UserNotFoundError()

    # Call Catalog Service API
    item = await catalog_service_client.get_item(item_id)
    if not item or item.quantity < quantity:
        raise InsufficientStockError()

    # Store in Cart Service's own database
    cart_item = await cart_repository.save(...)

    # Publish event for inventory reservation
    await event_bus.publish(ItemReservedEvent(...))
```

### No Data Ownership Boundaries

**Example: Everyone Accesses Everything**
```python
# app.py - Routes directly query all tables
@app.post("/users/{user_id}/cart")
def add_to_cart(user_id: UUID, item_id: UUID):
    # Single route touches 3 tables
    user = db.query(User).filter_by(id=user_id).first()
    item = db.query(Item).filter_by(id=item_id).first()
    cart = db.query(CartItem).filter_by(...).first()
```

**What's missing:**
- User data owned by User Service only
- Item data owned by Catalog Service only
- Cart data owned by Cart Service only
- Services communicate via APIs, not shared database

### Missing Anti-Corruption Layers

**Example: Direct Model Usage**
```python
# Route returns SQLAlchemy model directly
@app.get("/items/")
def get_items():
    return db.query(Item).all()  # SQLAlchemy model leaked to API!
```

**Problem:** API contract tied to database schema - cannot change independently.

**Should be:**
```python
# Catalog Service
@app.get("/items/")
def get_items() -> List[ItemResponse]:
    items = repository.list_all()
    return [ItemResponse.from_entity(item) for item in items]

# ItemResponse is API contract, decoupled from database
```

### What You'd Need to Split

**1. Separate Databases:**
```
User Service DB:
  - users table

Catalog Service DB:
  - items table

Cart Service DB:
  - cart_items table (with user_id and item_id as plain UUIDs, no FKs)
```

**2. API Contracts:**
```python
# User Service API
GET /users/{id}
POST /users
POST /users/authenticate

# Catalog Service API
GET /items
GET /items/{id}
POST /items
PUT /items/{id}/stock

# Cart Service API
GET /users/{user_id}/cart
POST /users/{user_id}/cart
```

**3. Event-Driven Communication:**
```python
# When item added to cart
Cart Service → publishes → ItemReservedEvent
Catalog Service → subscribes → decrements stock

# When order placed
Cart Service → publishes → OrderPlacedEvent
Inventory Service → subscribes → updates inventory
```

### Summary

The original code cannot be split because:
1. **Shared database** with foreign keys across domains
2. **No bounded contexts** - responsibilities mixed
3. **Cross-domain transactions** - one operation touches multiple domains
4. **Direct database access** - no service boundaries
5. **No API contracts** - internal models leaked everywhere

To enable microservices, we need Clean Architecture first.

## 2. Why does this project not adhere to clean architecture even though we have separate modules?

Having separate folders doesn't mean clean architecture. The violations are:

**Domain Layer Pollution:**
```python
# Entities importing SQLAlchemy (framework dependency in domain)
from sqlalchemy import Column, String
class User(Base):  # Domain depends on framework
    __tablename__ = "users"
```

**No Dependency Inversion:**
- Repositories are concrete implementations, not interfaces
- No abstract base classes defining contracts
- Use cases would directly import concrete repository implementations
- Dependencies point outward (domain → framework) instead of inward

**Business Logic in Wrong Layers:**
```python
# Repository functions contain business logic
def save_user(email, password):
    if find_user_by_email(email):  # Business rule in repository!
        raise HTTPException(...)  # HTTP concern in data layer!
    hashed = hash_password(password)  # Business logic here
```

**Missing Use Case Layer:**
- No explicit application business rules layer
- Business logic mixed between repositories and API routes
- Routes contain orchestration logic

**Framework Dependencies:**
- HTTPException used in domain/repository layer
- SQL Alchemy models mixed with domain entities
- FastAPI concerns leak into business logic

**Clean Architecture requires:**
- Domain entities with zero dependencies
- Use cases that orchestrate domain logic
- Repository interfaces (ports) defined by domain needs
- Adapters implement interfaces
- Dependencies always point inward

## 3. What would be your plan to refactor the project to stick to clean architecture?

### Phase 1: Foundation
1. **Create clean layer structure:**
   ```
   domain/entities/        # Pure business entities
   ports/repositories/     # Repository interfaces
   use_cases/             # Application business rules
   adapters/repositories/ # Repository implementations
   drivers/rest/          # FastAPI layer
   ```

2. **Extract domain entities:**
   - Remove SQLAlchemy from entity classes
   - Make them pure dataclasses
   - No framework dependencies

3. **Define repository interfaces (ports):**
   ```python
   class UserRepository(ABC):
       @abstractmethod
       async def save(self, user: User) -> User: pass
       @abstractmethod
       async def find_by_email(self, email: str) -> Optional[User]: pass
   ```

### Phase 2: Business Logic
4. **Create use cases:**
   - Extract business logic from repositories
   - Create command DTOs for input
   - Each use case has single responsibility
   ```python
   class CreateUserUseCase:
       def __init__(self, user_repo: UserRepository):
           self.user_repo = user_repo

       async def __call__(self, command: CreateUserCommand) -> User:
           # Business rules here
   ```

5. **Create domain exceptions:**
   - Replace HTTPException with domain exceptions
   - Map to HTTP at the boundary

### Phase 3: Adapters
6. **Implement repository adapters:**
   - Create in-memory implementations
   - Separate SQLAlchemy implementations if needed
   - Both implement same interface

7. **Create dependency injection:**
   - Use FastAPI's Depends or a good library for DI like dependency-injector
   - Wire up interfaces to implementations
   - Easy to swap implementations

### Phase 4: Drivers
8. **Refactor FastAPI layer:**
   - Routers only handle HTTP concerns
   - Map HTTP requests to commands
   - Call use cases
   - Map domain exceptions to HTTP responses -> exception_handlers.py

9. **Separate schemas from entities:**
   - Pydantic schemas for HTTP validation
   - Domain entities for business logic
   - Map between them at boundary

### Phase 5: Testing
10. **Write tests at each layer:**
    - Unit tests for use cases (mock repositories)
    - Integration tests for repositories
    - E2E tests for API endpoints

**Result:** I implemented all phases, achieving:
- 5 clean layers
- Dependency inversion
- 75 tests
- Zero framework dependencies in domain
- Easy to test, maintain, and extend

## 4. How can you make dependencies between modules more explicit?

### Use Abstract Base Classes
```python
# ports/repositories/user_repository.py
class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        pass
```

### Type Hints Everywhere
```python
class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository):  # Explicit dependency
        self.user_repo = user_repo
```

### Dependency Injection Container
```python
# drivers/rest/dependencies.py
@lru_cache
def get_user_repository() -> UserRepository:
    return InMemoryUserRepository()

def get_create_user_use_case(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repo)
```

### Clear Import Structure
```python
# Use cases only import from domain and ports
from be_task_ca.domain.entities.user import User
from be_task_ca.ports.repositories.user_repository import UserRepository

# Never import from adapters or drivers!
```

### Dependency Rule Enforcement
- Use tools like `import-linter` to enforce layer boundaries
- CI/CD checks to prevent circular dependencies
- 
### Interface Segregation
- Keep interfaces small and focused
- One interface per domain concept

### Explicit Constructor Injection
```python
# All dependencies via constructor (no hidden dependencies)
class AddItemToCartUseCase:
    def __init__(
        self,
        cart_repo: CartItemRepository,
        user_repo: UserRepository,
        item_repo: ItemRepository,
    ):
        self.cart_repo = cart_repo
        self.user_repo = user_repo
        self.item_repo = item_repo
```

### Benefits:
- Dependencies visible at compile time
- Easy to test (inject mocks)
- Easy to understand dataflow
- IDEs can help navigate
- Prevents circular dependencies

---
