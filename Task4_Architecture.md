# Task #4: Atomic Feature List & API Mapping

### 1. Category: Inventory Registry
| Atomic Feature | API Endpoint | Database Action |
| :--- | :--- | :--- |
| Add new asset | `POST /api/assets` | **INSERT** into `assets` table (tag_id, model, category). |
| View all assets | `GET /api/assets` | **SELECT * FROM** `assets` table. |
| Edit asset details | `PATCH /api/assets/:id` | **UPDATE** `assets` table WHERE `id` = :id. |
| Delete asset | `DELETE /api/assets/:id` | **DELETE** from `assets` table WHERE `id` = :id. |



### 2. Category: Allocation System
| Atomic Feature | API Endpoint | Database Action |
| :--- | :--- | :--- |
| Assign asset to employee | `POST /api/allocations` | **INSERT** into `allocations` (asset_id, emp_id). **UPDATE** `assets` status to 'Assigned'. |
| Process asset return | `PUT /api/allocations/:id` | **UPDATE** `return_date` in `allocations`. **UPDATE** `assets` status to 'Available'. |
| View asset history | `GET /api/assets/:id/history` | **SELECT** from `allocations` WHERE `asset_id` = :id. |



### 3. Category: Employee Management
| Atomic Feature | API Endpoint | Database Action |
| :--- | :--- | :--- |
| Add new employee | `POST /api/employees` | **INSERT** into `employees` (name, email, dept). |
| Search employee | `GET /api/employees/:id` | **SELECT** from `employees` WHERE `id` = :id. |
| Update employee info | `PATCH /api/employees/:id` | **UPDATE** `employees` table WHERE `id` = :id. |

### 4. Category: Maintenance Mode
| Atomic Feature | API Endpoint | Database Action |
| :--- | :--- | :--- |
| Flag for repair | `PATCH /api/assets/:id/maintenance` | **UPDATE** `assets` status to 'Repairing'. |
| Log repair issue | `POST /api/maintenance_logs` | **INSERT** into `maintenance_logs` (asset_id, description). |
| Resolve repair | `PUT /api/maintenance_logs/:id` | **UPDATE** `maintenance_logs` status. **UPDATE** `assets` status to 'Available'. |



### 5. Category: Search & Filters
| Atomic Feature | API Endpoint | Database Action |
| :--- | :--- | :--- |
| Filter by category | `GET /api/assets?type=laptop` | **SELECT** from `assets` WHERE `category` = 'laptop'. |
| Search by Barcode | `GET /api/assets/search?tag=123` | **SELECT** from `assets` WHERE `tag_id` = '123'. |