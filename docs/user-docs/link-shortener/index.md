utoria;---
sidebar_position: 8
---

# Link Shortener Module

The Link Shortener Module in SOLID provides URL shortening capabilities with tracking and management features.

## Overview

The Link Shortener enables:
- URL shortening
- Click tracking
- Expiry management
- Access control
- Analytics

## Features
<!-- 
### URL Management
- Custom short URLs
- Automatic generation
- URL validation
- Expiry settings
- Access restrictions

### Analytics
- Click tracking
- Geographic data
- Device information
- Referrer tracking
- Time-based stats

### Security
- Access control
- Rate limiting
- Domain whitelisting
- HTTPS enforcement
- Bot protection -->

<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1. URL Management</h4>
    <ul className="card-desc">
      <li>Custom short URLs</li>
      <li>Automatic generation</li>
      <li>URL validation</li>
      <li>Expiry settings</li>
      <li>Access restrictions</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2. Analytics</h4>
    <ul className="card-desc">
      <li>Click tracking</li>
      <li>Geographic data</li>
      <li>Device information</li>
      <li>Referrer tracking</li>
      <li>Time-based stats</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">3. Security</h4>
    <ul className="card-desc">
      <li>Access control</li>
      <li>Rate limiting</li>
      <li>Domain whitelisting</li>
      <li>HTTPS enforcement</li>
      <li>Bot protection</li>
    </ul>
  </div>

</div>




## Configuration

### Basic Setup

```json
{
  "shortener": {
    "domain": "s.example.com",
    "length": 6,
    "charset": "alphanumeric",
    "https": true,
    "tracking": {
      "enabled": true,
      "anonymize": true
    }
  }
}
```

### URL Creation

```json
{
  "url": {
    "original": "https://very-long-domain.com/with/very/long/path?and=parameters",
    "options": {
      "custom": "promo2024",
      "expiry": "2024-12-31",
      "maxClicks": 1000,
      "tracking": true,
      "password": "optional-access-code"
    }
  }
}
```

## Usage

### Creating Short URLs

```javascript
// Create short URL
const shortUrl = await createShortUrl({
  url: "https://example.com/long/path",
  options: {
    expiry: "30d",
    tracking: true
  }
});

// Create with custom path
const customUrl = await createShortUrl({
  url: "https://example.com/long/path",
  options: {
    path: "promo",
    expiry: "2024-12-31"
  }
});
```

### Managing URLs

```javascript
// Update URL
await updateShortUrl("abc123", {
  expiry: "2024-12-31",
  maxClicks: 500
});

// Delete URL
await deleteShortUrl("abc123");

// Get URL stats
const stats = await getUrlStats("abc123");
```

## Analytics

### Click Tracking

```json
{
  "url": "abc123",
  "clicks": [
    {
      "timestamp": "2024-01-01T12:00:00Z",
      "ip": "anonymized",
      "country": "US",
      "city": "San Francisco",
      "device": "mobile",
      "browser": "Chrome",
      "referrer": "twitter.com"
    }
  ],
  "summary": {
    "totalClicks": 150,
    "uniqueClicks": 120,
    "countries": {
      "US": 80,
      "UK": 40,
      "Other": 30
    }
  }
}
```

### Reporting

```json
{
  "report": {
    "timeframe": {
      "start": "2024-01-01",
      "end": "2024-01-31"
    },
    "metrics": [
      "clicks",
      "unique_visitors",
      "countries",
      "devices"
    ],
    "format": "pdf",
    "schedule": "monthly"
  }
}
```

## Best Practices
<!-- 
1. **URL Management**
   - Use HTTPS only
   - Set appropriate expiry
   - Monitor usage patterns
   - Clean up old URLs
   - Document purpose

2. **Security**
   - Enable rate limiting
   - Validate URLs
   - Monitor abuse
   - Regular audits
   - Secure storage

3. **Analytics**
   - Respect privacy
   - Aggregate data
   - Regular backups
   - Monitor trends
   - Clean old data

4. **Performance**
   - Cache responses
   - Optimize redirects
   - Monitor latency
   - Scale horizontally
   - Regular maintenance -->


<div className="feature-grid">
  <div className="feature-card">
    <h4 className="card-title">1. URL Management</h4>
    <ul className="card-desc">
      <li>Use HTTPS only</li>
      <li>Set appropriate expiry</li>
      <li>Monitor usage patterns</li>
      <li>Clean up old URLs</li>
      <li>Document purpose</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2. Security</h4>
    <ul className="card-desc">
      <li>Enable rate limiting</li>
      <li>Validate URLs</li>
      <li>Monitor abuse</li>
      <li>Regular audits</li>
      <li>Secure storage</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">3. Analytics</h4>
    <ul className="card-desc">
      <li>Respect privacy</li>
      <li>Aggregate data</li>
      <li>Regular backups</li>
      <li>Monitor trends</li>
      <li>Clean old data</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">4. Performance</h4>
    <ul className="card-desc">
      <li>Cache responses</li>
      <li>Optimize redirects</li>
      <li>Monitor latency</li>
      <li>Scale horizontally</li>
      <li>Regular maintenance</li>
    </ul>
  </div>

</div>



## Common Use Cases

### Marketing Campaigns

```json
{
  "campaign": {
    "name": "summer_promo",
    "urls": [
      {
        "original": "https://example.com/summer-sale",
        "custom": "summer24",
        "expiry": "2024-09-01",
        "tracking": {
          "utmSource": "social",
          "utmMedium": "twitter",
          "utmCampaign": "summer_2024"
        }
      }
    ]
  }
}
```

### Document Sharing

```json
{
  "document": {
    "original": "https://storage.example.com/documents/very-long-file-name.pdf",
    "options": {
      "expiry": "7d",
      "maxClicks": 1,
      "password": "secure123",
      "notification": {
        "email": "uploader@example.com",
        "events": ["clicked", "expired"]
      }
    }
  }
}
```

### API Integration

```json
{
  "integration": {
    "service": "email_templates",
    "config": {
      "autoShorten": true,
      "template": {
        "prefix": "email",
        "expiry": "30d",
        "tracking": true
      }
    }
  }
}
