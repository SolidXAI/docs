---
sidebar_position: 7
---

# Report Templates

The Report Template Module in SOLID allows you to configure HTML to PDF report creation with dynamic content and placeholder replacement.

## Overview

Report Templates enable:
- Dynamic PDF generation
- Template-based layouts
- Variable replacement
- Custom styling
- Automated generation

## Features

### Template Design
- HTML-based templates
- CSS styling support
- Dynamic content areas
- Header and footer
- Page numbering

### Data Integration
- Dynamic data binding
- Multiple data sources
- Conditional sections
- Calculated fields
- Aggregations

### Output Options
- PDF generation
- Multiple paper sizes
- Custom margins
- Orientation options
- Quality settings

## Template Creation

### Basic Structure

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 30px;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{reportTitle}}</h1>
        <p>Generated on: {{generationDate}}</p>
    </div>

    <div class="content">
        {% for section in sections %}
        <h2>{{section.title}}</h2>
        <table>
            <thead>
                <tr>
                    {% for header in section.headers %}
                    <th>{{header}}</th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for row in section.data %}
                <tr>
                    {% for cell in row %}
                    <td>{{cell}}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endfor %}
    </div>

    <div class="footer">
        Page {{pageNumber}} of {{totalPages}}
    </div>
</body>
</html>
```

### Template Configuration

```json
{
  "name": "monthly_sales_report",
  "description": "Monthly sales report with product performance",
  "template": "templates/sales_report.html",
  "options": {
    "format": "A4",
    "orientation": "portrait",
    "margin": {
      "top": "30mm",
      "right": "20mm",
      "bottom": "30mm",
      "left": "20mm"
    }
  },
  "variables": {
    "reportTitle": {
      "type": "string",
      "required": true
    },
    "generationDate": {
      "type": "date",
      "format": "YYYY-MM-DD"
    },
    "sections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "title": "string",
          "headers": "array",
          "data": "array"
        }
      }
    }
  }
}
```

## Usage

### Generating Reports

```javascript
// Generate report
const report = await generateReport({
  template: "monthly_sales_report",
  data: {
    reportTitle: "Monthly Sales Report - January 2024",
    generationDate: "2024-02-01",
    sections: [
      {
        title: "Top Products",
        headers: ["Product", "Units Sold", "Revenue"],
        data: [
          ["Product A", "150", "$3,000"],
          ["Product B", "120", "$2,400"]
        ]
      }
    ]
  },
  output: {
    filename: "sales_report_jan_2024.pdf"
  }
});
```

### Scheduling Reports

```json
{
  "schedule": {
    "name": "monthly_sales",
    "template": "monthly_sales_report",
    "frequency": "monthly",
    "day": 1,
    "time": "00:00",
    "timezone": "UTC",
    "distribution": {
      "email": {
        "to": ["manager@example.com"],
        "subject": "Monthly Sales Report - {{month}}"
      }
    }
  }
}
```

## Best Practices

1. **Template Design**
   - Use responsive layouts
   - Optimize for printing
   - Consider page breaks
   - Test with various data
   - Include proper margins

2. **Data Handling**
   - Validate input data
   - Handle missing values
   - Format numbers/dates
   - Consider large datasets
   - Implement timeouts

3. **Performance**
   - Optimize images
   - Minimize CSS
   - Cache templates
   - Batch processing
   - Monitor memory usage

4. **Output**
   - Set appropriate DPI
   - Optimize file size
   - Test across viewers
   - Implement compression
   - Secure storage

## Common Use Cases

### Financial Reports
```json
{
  "name": "financial_statement",
  "template": "templates/financial.html",
  "options": {
    "format": "A4",
    "orientation": "portrait"
  },
  "sections": [
    {
      "name": "income_statement",
      "title": "Income Statement",
      "type": "table"
    },
    {
      "name": "balance_sheet",
      "title": "Balance Sheet",
      "type": "table"
    }
  ]
}
```

### Analytics Reports
```json
{
  "name": "analytics_report",
  "template": "templates/analytics.html",
  "options": {
    "format": "A4",
    "orientation": "landscape"
  },
  "sections": [
    {
      "name": "traffic_overview",
      "type": "chart",
      "chartType": "line"
    },
    {
      "name": "conversion_metrics",
      "type": "table"
    }
  ]
}
```

### Inventory Reports
```json
{
  "name": "inventory_status",
  "template": "templates/inventory.html",
  "options": {
    "format": "A4",
    "orientation": "portrait"
  },
  "sections": [
    {
      "name": "stock_levels",
      "type": "table",
      "alerts": {
        "lowStock": {
          "threshold": 10,
          "highlight": "red"
        }
      }
    }
  ]
}
