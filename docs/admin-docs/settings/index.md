---
sidebar_position: 9
---

# Other Settings

SOLID provides various system-wide settings and configurations to manage your application's behavior and functionality.

## Overview

The Settings module includes:
- List of Values management
- Message and Queue logs
- Import/Export job tracking
- Saved views management
- System configurations

## List of Values

### Purpose
- Manage reusable value lists
- Centralize dropdown options
- Maintain data consistency
- Support multiple languages
- Version control values

### Configuration

```json
{
  "list": {
    "name": "status_codes",
    "description": "Common status codes for orders",
    "type": "string",
    "values": [
      {
        "value": "pending",
        "label": {
          "en": "Pending",
          "es": "Pendiente"
        }
      },
      {
        "value": "processing",
        "label": {
          "en": "Processing",
          "es": "Procesando"
        }
      },
      {
        "value": "completed",
        "label": {
          "en": "Completed",
          "es": "Completado"
        }
      }
    ]
  }
}
```

## Message & Queue Logs

### Message Log
- Track system messages
- Monitor notifications
- Debug delivery issues
- View message history
- Export log data

```json
{
  "messageLog": {
    "filters": {
      "type": ["email", "sms"],
      "status": ["sent", "failed"],
      "dateRange": {
        "start": "2024-01-01",
        "end": "2024-01-31"
      }
    },
    "columns": [
      "timestamp",
      "type",
      "recipient",
      "subject",
      "status",
      "error"
    ]
  }
}
```

### Queue Log
- Monitor job queues
- Track job status
- View error details
- Retry failed jobs
- Performance metrics

```json
{
  "queueLog": {
    "queues": {
      "email": {
        "status": "active",
        "jobs": {
          "pending": 5,
          "processing": 2,
          "failed": 1
        },
        "metrics": {
          "avgProcessingTime": "2.5s",
          "throughput": "100/min"
        }
      }
    }
  }
}
```

## Import & Export Jobs

### Import Management
- Track import progress
- Validate data
- Handle errors
- Map fields
- Schedule imports

```json
{
  "import": {
    "source": {
      "type": "csv",
      "file": "customers.csv",
      "encoding": "UTF-8"
    },
    "mapping": {
      "email": "Email Address",
      "firstName": "First Name",
      "lastName": "Last Name"
    },
    "options": {
      "skipHeader": true,
      "batchSize": 1000,
      "onError": "skip"
    }
  }
}
```

### Export Management
- Configure exports
- Format options
- Schedule exports
- Delivery options
- Track progress

```json
{
  "export": {
    "target": {
      "type": "csv",
      "filename": "sales_report_{{date}}"
    },
    "data": {
      "query": {
        "model": "sales",
        "filters": {
          "date": {
            "gte": "{{startDate}}",
            "lte": "{{endDate}}"
          }
        }
      }
    },
    "schedule": {
      "frequency": "monthly",
      "day": 1,
      "time": "00:00",
      "timezone": "UTC"
    }
  }
}
```

## Saved Views

### View Management
- Save custom views
- Share with teams
- Set defaults
- Manage permissions
- Version control

```json
{
  "savedView": {
    "name": "High Value Orders",
    "resource": "orders",
    "type": "list",
    "config": {
      "filters": {
        "total": {
          "gte": 1000
        },
        "status": ["pending", "processing"]
      },
      "sort": [
        {
          "field": "total",
          "direction": "desc"
        }
      ],
      "columns": [
        "orderNumber",
        "customer",
        "total",
        "status",
        "createdAt"
      ]
    },
    "sharing": {
      "roles": ["sales_manager", "account_executive"],
      "isDefault": false
    }
  }
}
```

## Best Practices

<!-- 1. **List of Values**
   - Use meaningful names
   - Document purpose
   - Consider translations
   - Regular reviews
   - Version control

2. **Logging**
   - Set retention periods
   - Monitor storage
   - Regular cleanup
   - Error alerts
   - Performance monitoring

3. **Import/Export**
   - Validate data
   - Handle errors gracefully
   - Schedule off-peak
   - Monitor resources
   - Backup data

4. **Saved Views**
   - Clear naming
   - Document purpose
   - Regular cleanup
   - Test performance
   - Review permissions -->


  <div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1. List of Values</h4>
    <ul className="card-desc">
      <li>Use meaningful names</li>
      <li>Document purpose</li>
      <li>Consider translations</li>
      <li>Regular reviews</li>
      <li>Version control</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2. Logging</h4>
    <ul className="card-desc">
      <li>Set retention periods</li>
      <li>Monitor storage</li>
      <li>Regular cleanup</li>
      <li>Error alerts</li>
      <li>Performance monitoring</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">3. Import/Export</h4>
    <ul className="card-desc">
      <li>Validate data</li>
      <li>Handle errors gracefully</li>
      <li>Schedule off-peak</li>
      <li>Monitor resources</li>
      <li>Backup data</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">4. Saved Views</h4>
    <ul className="card-desc">
      <li>Clear naming</li>
      <li>Document purpose</li>
      <li>Regular cleanup</li>
      <li>Test performance</li>
      <li>Review permissions</li>
    </ul>
  </div>

</div>


## Common Operations

### Managing Lists

```json
{
  "operation": "createList",
  "list": {
    "name": "priority_levels",
    "values": [
      {
        "value": "high",
        "label": "High Priority",
        "color": "red"
      },
      {
        "value": "medium",
        "label": "Medium Priority",
        "color": "yellow"
      },
      {
        "value": "low",
        "label": "Low Priority",
        "color": "green"
      }
    ]
  }
}
```

### Monitoring Queues

```json
{
  "operation": "getQueueMetrics",
  "queues": ["email", "sms", "notifications"],
  "metrics": [
    "jobCount",
    "processingTime",
    "errorRate",
    "throughput"
  ],
  "timeframe": {
    "last": "24h"
  }
}
```

### Managing Imports

```json
{
  "operation": "importData",
  "config": {
    "source": {
      "type": "excel",
      "file": "products.xlsx",
      "sheet": "Sheet1"
    },
    "target": {
      "model": "products",
      "mode": "upsert",
      "key": "sku"
    },
    "validation": {
      "stopOnError": false,
      "errorThreshold": 0.1
    }
  }
}
```

### Creating Views

```json
{
  "operation": "createView",
  "view": {
    "name": "Active Projects",
    "resource": "projects",
    "type": "kanban",
    "config": {
      "groupBy": "status",
      "columns": ["todo", "in_progress", "review", "done"],
      "cardFields": [
        "title",
        "assignee",
        "dueDate",
        "priority"
      ]
    }
  }
}
