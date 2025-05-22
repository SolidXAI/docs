---
sidebar_position: 2
---

# Model Management

Models represent the structure of your data within a module. Each model defines a specific type of data and its relationships.

### Creating a Model

To create a new model:

1. Navigate to your module in the App Builder
2. Click "New Model"
3. Configure the model settings

### Model Configuration Options

| Setting | Description |
|---------|-------------|
| Name | Internal name of the model (e.g., "customer") |
| Display Name | User-friendly name shown in the UI |
| Description | Brief description of the model's purpose |
| Soft Delete | Enable/disable soft deletion for records |
| Audit Tracking | Track creation, updates, and deletion of records |
| Internationalization | Enable multi-language support for records |

### Advanced Features
<!-- 
### Soft Delete
When enabled, records are marked as deleted instead of being permanently removed from the database. This provides:
- Record recovery capability
- Maintenance of data integrity
- Preservation of historical data
- Ability to restore accidentally deleted records

### Audit Tracking
Comprehensive tracking of record changes:
- Creation timestamp and user
- Modification timestamp and user
- Deletion timestamp and user (with soft delete)
- Field-level change history
- Comments and annotations

### Internationalization
Built-in support for multiple languages:
- Define translatable fields
- Manage translations per record
- Automatic language detection
- Language fallback configuration
- Translation import/export -->



### Soft Delete
<div className="feature-grid">
   <div className="feature-card-medium">
   When enabled, records are marked as deleted instead of being permanently removed from the database. This provides:
   - Record recovery capability
   - Maintenance of data integrity
   - Preservation of historical data
   - Ability to restore accidentally deleted records
   </div>
</div>

### Audit Tracking
<div className="feature-grid">
   <div className="feature-card-medium">
   Comprehensive tracking of record changes:
   - Creation timestamp and user
   - Modification timestamp and user
   - Deletion timestamp and user (with soft delete)
   - Field-level change history
   - Comments and annotations
   </div>
</div>

### Internationalization
<div className="feature-grid">
   <div className="feature-card-medium">
   Built-in support for multiple languages:
   - Define translatable fields
   - Manage translations per record
   - Automatic language detection
   - Language fallback configuration
   - Translation import/export

   </div>
</div>

### Model Relationships

Models can be related to each other in various ways:

<!-- ### One-to-One
- Link two records uniquely
- Example: User profile linked to user account

### One-to-Many
- One record relates to multiple records
- Example: Customer with multiple orders

### Many-to-Many
- Records can be related to multiple records
- Example: Products in multiple categories -->


<div className="feature-grid">
   

   <div className="feature-card">
      <h4 className="card-title">
         #### 1 One-to-One
      </h4>
      <ul className="card-desc">
         <li>Link two records uniquely</li>
         <li>Example: User profile linked to user account</li>
      </ul>
   </div>

   <div className="feature-card">
      <h4 className="card-title">
         #### 2 One-to-Many
      </h4>
      <ul className="card-desc">
         <li>One record relates to multiple records</li>
         <li>Example: Customer with multiple orders</li>
      </ul>
   </div>

   <div className="feature-card">
      <h4 className="card-title">
         #### 3 Many-to-Many
      </h4>
      <ul className="card-desc">
         <li>Records can be related to multiple records</li>
         <li>Example: Products in multiple categories</li>
      </ul>
   </div>
</div>


### Best Practices

<!-- 1. **Data Modeling**
   - Plan your model structure carefully
   - Consider relationships between models
   - Use appropriate field types

2. **Performance**
   - Enable features selectively
   - Consider indexing requirements
   - Plan for scalability

3. **Data Integrity**
   - Use soft delete when appropriate
   - Enable audit tracking for sensitive data
   - Plan backup strategies

4. **Internationalization**
   - Plan language requirements early
   - Consider regional differences
   - Document translation processes -->



<div className="feature-grid">

   <div className="feature-card">
      <h4 className="card-title">
         **1 Data Modeling**
      </h4>
      <ul className="card-desc">
         <li>Plan your model structure carefully</li>
         <li>Consider relationships between models</li>
         <li>Use appropriate field types</li>
      </ul>
   </div>

   <div className="feature-card">
      <h4 className="card-title">
          **2 Performance**
      </h4>
      <ul className="card-desc">
         <li>Enable features selectively</li>
         <li>Consider indexing requirements</li>
         <li>Plan for scalability</li>
      </ul>
   </div>
    <div className="feature-card">
      <h4 className="card-title">
        **3 Data Integrity**
      </h4>
      <ul className="card-desc">
         <li>Use soft delete when appropriate</li>
         <li>Enable audit tracking for sensitive data</li>
         <li>Plan backup strategies</li>
      </ul>
   </div>
   
   <div className="feature-card">
      <h4 className="card-title">
         **4 Internationalization**
      </h4>
      <ul className="card-desc">
         <li>Plan language requirements early</li>
         <li>Consider regional differences</li>
         <li>Document translation processes</li>
      </ul>
   </div>
</div>


