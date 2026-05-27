---
title: Activate Institute Portal
description: Learn how to activate an institute's fee portal and make it live for students and parents.
summary: Complete guide to activating institute portals with automatic DNS and web server configuration
keywords: [institute activation, portal deployment, DNS configuration, multi-tenant setup]
concerns: Infrastructure provisioning, domain management, activation workflow
---

ls -la /etc/nginx/sites-available/{domain}.conf

# Check symlink exists
ls -la /etc/nginx/sites-enabled/{domain}.conf

# Verify Nginx configuration is valid
sudo nginx -t

# Check Nginx is running
sudo systemctl status nginx
```

All commands should succeed without errors.

**Step 12: Test Portal Access**

**Method 1: Browser Test**
- Open a web browser
- Navigate to `http://{domain}` (e.g., `http://stmary.solidx.edu`)
- The student portal should load
- You should see the institute's fee payment interface

**Method 2: Curl Test**
```bash
curl -I http://{domain}
```
- Should return `HTTP/1.1 200 OK` or `HTTP/1.1 302 Found`
- Should not return `404 Not Found` or connection errors

**Expected Result:**
- Portal loads successfully
- No certificate warnings (if HTTPS is configured)
- Institute branding appears correct
- No error messages visible

**Step 13: Notify Institute Admin**

Once activation is verified:
- Contact the Institute Admin via email or phone
- Provide the live portal URL
- Share any login credentials or setup instructions
- Confirm they can access the admin panel

#### Phase 4: Troubleshooting Failed Activation

If activation fails or portal is not accessible:

**Issue: "Failed to activate institute" Error**

**Possible Causes:**
1. Missing `PORTAL_CNAME_DOMAIN` environment variable
2. DNS provider configuration error
3. Nginx reload failure
4. Insufficient server permissions

**Solutions:**
1. Check environment variables on server:
   ```bash
   echo $PORTAL_CNAME_DOMAIN
   ```
   - Should return a valid domain
   - If empty, set in `.env` file or server configuration

2. Check DNS provider configuration:
   ```bash
   # For Route53
   aws route53 list-hosted-zones
   # Verify hosted zone exists

   # For hosts file
   ls -la /etc/hosts
   # Verify file is writable
   ```

3. Check Nginx status:
   ```bash
   sudo nginx -t
   sudo systemctl status nginx
   sudo journalctl -u nginx -n 50
   ```
   - Look for syntax errors or reload failures

4. Check application logs:
   ```bash
   # API logs
   pm2 logs solid-api
   # Or check log files
   tail -f /path/to/api/logs/error.log
   ```

**Issue: Portal Returns 404 Not Found**

**Possible Causes:**
1. Nginx configuration not created
2. Nginx not reloaded after configuration
3. Virtual host not enabled (symlink missing)

**Solutions:**
1. Verify configuration file exists:
   ```bash
   cat /etc/nginx/sites-available/{domain}.conf
   ```

2. Verify symlink exists:
   ```bash
   ls -la /etc/nginx/sites-enabled/ | grep {domain}
   ```

3. Manually reload Nginx:
   ```bash
   sudo systemctl reload nginx
   ```

**Issue: DNS Not Resolving**

**Possible Causes:**
1. DNS record not created
2. DNS propagation delay (Route53)
3. Wrong hosted zone (Route53)
4. Hosts file not updated (local)

**Solutions:**
1. For Route53, check record exists:
   ```bash
   aws route53 list-resource-record-sets --hosted-zone-id {zone-id}
   ```

2. For hosts file, check entry:
   ```bash
   cat /etc/hosts | grep {domain}
   ```

3. Wait 10-15 minutes for DNS propagation (production)

4. Flush DNS cache on client:
   ```bash
   # macOS
   sudo dscacheutil -flushcache

   # Windows
   ipconfig /flushdns

   # Linux
   sudo systemd-resolve --flush-caches
   ```

**Issue: Portal Loads But Shows Wrong Institute**

**Possible Causes:**
1. Nginx upstream configuration pointing to wrong instance
2. Frontend routing not matching domain to institute

**Solutions:**
1. Verify Nginx proxy configuration:
   ```bash
   cat /etc/nginx/sites-available/{domain}.conf
   ```
   - Check `proxy_pass` directive
   - Should point to `EDU_FRONTEND_UPSTREAM`

2. Check frontend routing logic in application code

3. Verify `hostedPagePrefix` uniqueness in database

### Deactivating an Institute

If you need to take a portal offline:

#### Deactivation Process

**Step 1: Navigate to Active Institute**
- Open the institute record
- Verify status is currently "Active"
- "Deactivate Institute" button should be visible

**Step 2: Initiate Deactivation**
- Click "Deactivate Institute" button (⊗ icon)
- Confirmation dialog appears:
  - Header: "Deactivate institute?"
  - Message: "Clicking Ok below will Deactivate this institute, are you sure you want to continue?"

**Step 3: Confirm Deactivation**
- Click "Ok" to proceed
- System will:
  1. Remove Nginx virtual host configuration
  2. Remove DNS CNAME record
  3. Set status to "InActive"
  4. Create audit trail entry

**Step 4: Verify Deactivation**
- Success message: "institute Deactivated successfully."
- Status changes to "InActive"
- "Activate Institute" button reappears
- Portal becomes inaccessible (404 or connection error)

#### When to Deactivate

**Valid Reasons:**
- Institute contract ended
- Switching to different platform
- Temporary suspension due to payment issues
- Maintenance or configuration changes needed
- Institute closure

**Important:** Deactivation only removes infrastructure - it does not delete data. Student records, payment history, and configuration remain in the database and can be reactivated later.

### Technical Implementation Details

This section explains how the activation system works under the hood.

#### Backend Service Implementation

**File:** `solid-api/src/fees-portal/services/institute.service.ts`

**Activation Method:** `activateInstitutePortal(id: number)`

```typescript
async activateInstitutePortal(id: number) {
  // 1. Retrieve institute record
  const institute = await this.findOne(id, {});

  // 2. Construct domain name
  const baseDoamin = process.env.EDU_BASE_DOMAIN || 'solidx.edu';
  const domainName = `${institute.hostedPagePrefix}-${baseDoamin}`;

  // 3. Create Nginx virtual host
  await this.nginxVirtualHostProvider.makeVirtualHost(domainName);

  // 4. Create DNS CNAME record
  const portalCnameDomain = process.env.PORTAL_CNAME_DOMAIN;
  if (!portalCnameDomain) {
    throw new NotAcceptableException('PORTAL_CNAME_DOMAIN env var not configured');
  }
  await this.dns.createCnameRecord(domainName, portalCnameDomain, 300);

  // 5. Update status
  institute.status = 'Active';
  await this.repo.save(institute);

  // 6. Create audit entry
  const postMessageOnActivate: PostChatterMessageDto = {
    coModelEntityId: institute.id,
    coModelName: 'institute',
    messageBody: `
### Institute Activated
Institute is now live on domain: <a href="${domainName}" target="_blank" rel="noopener noreferrer">${domainName}</a>
    `
  };
  await this.chatterMessageService.postMessage(postMessageOnActivate);

  return { message: 'Institute activated successfully' };
}
```

**Key Points:**
- Domain name constructed from `hostedPagePrefix` and `EDU_BASE_DOMAIN`
- Infrastructure provisioning happens before database update
- If any step fails, exception is thrown (status remains "InActive")
- Audit trail created after successful activation

**Deactivation Method:** `deActivateInstitutePortal(id: number)`

```typescript
async deActivateInstitutePortal(id: number) {
  const institute = await this.findOne(id, {});
  const baseDoamin = process.env.EDU_BASE_DOMAIN || 'solidx.edu';
  const domainName = `${institute.hostedPagePrefix}-${baseDoamin}`;

  // 1. Remove Nginx virtual host
  await this.nginxVirtualHostProvider.removeVirtualHost(domainName);

  // 2. Remove DNS record
  const portalCnameDomain = process.env.PORTAL_CNAME_DOMAIN;
  if (!portalCnameDomain) {
    throw new NotAcceptableException('PORTAL_CNAME_DOMAIN env var not configured');
  }
  await this.dns.removeCnameRecord(domainName, portalCnameDomain);

  // 3. Update status
  institute.status = 'InActive';
  await this.repo.save(institute);

  // 4. Create audit entry
  const postMessageOnDeActivate: PostChatterMessageDto = {
    coModelEntityId: institute.id,
    coModelName: 'institute',
    messageBody: '### Institute De Activated'
  };
  await this.chatterMessageService.postMessage(postMessageOnDeActivate);

  return { message: 'Institute de activated successfully' };
}
```

#### API Endpoints

**File:** `solid-api/src/fees-portal/controllers/institute.controller.ts`

**Activation Endpoint:**
```typescript
@ApiBearerAuth("jwt")
@Post('activate/:id')
async activateFeePortal(@Param('id') id: number) {
  return this.service.activateInstitutePortal(id);
}
```

**URL:** `POST /api/institute/activate/{id}`

**Authentication:** Requires JWT Bearer token

**Parameters:**
- `id` (path parameter): Institute ID to activate

**Response (Success):**
```json
{
  "message": "Institute activated successfully"
}
```

**Response (Error):**
```json
{
  "statusCode": 406,
  "message": "PORTAL_CNAME_DOMAIN env var not configured",
  "error": "Not Acceptable"
}
```

**Deactivation Endpoint:**
```typescript
@ApiBearerAuth("jwt")
@Post('deactivate/:id')
async deactivateFeePortal(@Param('id') id: number) {
  return this.service.deActivateInstitutePortal(id);
}
```

**URL:** `POST /api/institute/deactivate/{id}`

**Authentication:** Requires JWT Bearer token

**Parameters:**
- `id` (path parameter): Institute ID to deactivate

**Response:** Same structure as activation endpoint

#### Nginx Virtual Host Provider

**File:** `solid-api/src/fees-portal/services/ubuntu-nginx-virtual-host-provider.ts`

**Purpose:** Manages Nginx server block configurations for institute domains

**Method: `makeVirtualHost(domainName: string)`**

**What It Does:**
1. Validates domain name syntax (conservative regex for ASCII hostnames)
2. Renders Nginx server block template with:
   - Server name: `{domainName}`
   - Listen: Port 80
   - Proxy pass: `{EDU_FRONTEND_UPSTREAM}`
   - Proxy headers: Host, X-Real-IP, X-Forwarded-For, X-Forwarded-Proto
3. Writes configuration to `/etc/nginx/sites-available/{domainName}.conf`
4. Creates symlink in `/etc/nginx/sites-enabled/{domainName}.conf`
5. Tests Nginx configuration: `nginx -t`
6. Reloads Nginx: `systemctl reload nginx`

**Server Block Template:**
```nginx
server {
    listen 80;
    server_name {domainName};

    location / {
        proxy_pass {EDU_FRONTEND_UPSTREAM};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Method: `removeVirtualHost(domainName: string)`**

**What It Does:**
1. Removes symlink from `/etc/nginx/sites-enabled/{domainName}.conf`
2. Removes configuration from `/etc/nginx/sites-available/{domainName}.conf`
3. Tests Nginx configuration: `nginx -t`
4. Reloads Nginx: `systemctl reload nginx`

**Error Handling:**
- Throws exception if domain name is invalid
- Throws exception if Nginx test fails
- Throws exception if Nginx reload fails
- All operations are atomic (rollback on failure)

#### DNS Management - Route53 Provider

**File:** `solid-api/src/fees-portal/services/route53-website-dns.manager.ts`

**Purpose:** Manages DNS CNAME records using AWS Route53

**Method: `createCnameRecord(name: string, value: string, ttl: number)`**

**What It Does:**
1. Constructs Route53 API request:
   - Action: UPSERT (create or update)
   - Type: CNAME
   - Name: `{name}` (e.g., `stmary.solidx.edu`)
   - Value: `{value}` (PORTAL_CNAME_DOMAIN)
   - TTL: `{ttl}` seconds (default: 300)
2. Calls Route53 API: `changeResourceRecordSets`
3. Waits for change to propagate (async)

**Prerequisites:**
- AWS credentials configured (IAM role or environment variables)
- Route53 hosted zone ID provided to constructor
- Hosted zone must match `EDU_BASE_DOMAIN`

**Method: `removeCnameRecord(name: string, value: string)`**

**What It Does:**
1. Constructs Route53 API request with DELETE action
2. Calls Route53 API to remove the CNAME record
3. Waits for change to propagate

#### DNS Management - Hosts File Provider

**File:** `solid-api/src/fees-portal/services/hosts-file-website-dns.manager.ts`

**Purpose:** Manages DNS entries in local `/etc/hosts` file for development

**Method: `createCnameRecord(name: string, value: string, ttl: number)`**

**What It Does:**
1. Reads `/etc/hosts` file
2. Checks if entry already exists
3. If not, appends entry:
   ```
   127.0.0.1  {name} # solidx-dns
   ```
4. Writes updated content back to `/etc/hosts`

**Method: `removeCnameRecord(name: string, value: string)`**

**What It Does:**
1. Reads `/etc/hosts` file
2. Filters out lines containing `{name} # solidx-dns`
3. Writes filtered content back to `/etc/hosts`

**Prerequisites:**
- Application runs with sudo/root privileges
- `/etc/hosts` file is writable
- File system allows file modification

**Marker System:**
- All entries tagged with `# solidx-dns` comment
- Allows safe removal without affecting other entries
- Prevents duplicate entries

#### DNS Provider Selection

**File:** `solid-api/src/fees-portal/fees-portal.module.ts`

```typescript
const which = (cfg.get<string>('DNS_PROVIDER') ?? 'hosts').toLowerCase();
if (which === 'route53') {
  return new Route53WebsiteDnsManager(hostedZoneId);
}
return new HostsFileWebsiteDnsManager();
```

**Logic:**
- Checks `DNS_PROVIDER` environment variable
- If `"route53"`: Uses Route53WebsiteDnsManager
- If `"hosts"` or not set: Uses HostsFileWebsiteDnsManager
- Case-insensitive comparison

**Recommended Setup:**
- **Production:** `DNS_PROVIDER=route53`
- **Local Development:** `DNS_PROVIDER=hosts` (or omit)

#### UI Components

**Activate Button Component:**

**File:** `solid-ui/app/admin/extensions/headerButtons/activate-portal.tsx`

**Component:** `InstituteActivateById`

```typescript
export default function InstituteActivateById({ formData, refetch, onClose }: Props) {
  const session = useSession();
  const [loading, setLoading] = useState(false);

  const handleActivate = async () => {
    setLoading(true);
    try {
      // Call activation API
      const response = await fetch(`/api/institute/activate/${formData.id}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${session.data.user.accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) throw new Error('Activation failed');

      // Update status in UI
      await fetch(`/api/institute/${formData.id}`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${session.data.user.accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: 'Active' }),
      });

      toast.success('Institute activated successfully.');
      onClose();
      refetch();
    } catch (error) {
      toast.error('Failed to activate institute.');
    } finally {
      setLoading(false);
    }
  };

  return (
    
  );
}
```

**Key Features:**
- Confirmation dialog prevents accidental activation
- Shows loading state during provisioning
- Success/error toast notifications
- Automatic form refresh after activation
- JWT authentication with session token

**Deactivate Button Component:**

**File:** `solid-ui/app/admin/extensions/headerButtons/deActivate-portal.tsx`

**Component:** `InstituteDeactivateById`

Similar structure to activate button, but:
- Different confirmation message
- Calls `/api/institute/deactivate/{id}` endpoint
- Sets status to "InActive" on success

#### Conditional UI - Edit Handler

**File:** `solid-ui/app/admin/extensions/instituteEditHandler.ts`

```typescript
const instituteEditHandler = async (event: any) => {
  const { viewMetadata, formData, fieldsMetadata } = event;
  const { status } = formData || {};

  const layoutManager = new SolidViewLayoutManager(viewMetadata.layout);

  if(status === "InActive"){
    layoutManager.updateNodeAttributes("InstituteActivateById", { visible: true });
    layoutManager.updateNodeAttributes("InstituteDeactivateById", { visible: false });
  } else if(status === "Active"){
    layoutManager.updateNodeAttributes("InstituteActivateById", { visible: false });
    layoutManager.updateNodeAttributes("InstituteDeactivateById", { visible: true });
  }

  return {
    layoutChanged: true,
    dataChanged: false,
    newLayout: layoutManager.getLayout()
  };
};

export default instituteEditHandler;
```

**Purpose:** Controls button visibility based on current status

**Logic:**
- When status = "InActive": Show "Activate" button, hide "Deactivate" button
- When status = "Active": Show "Deactivate" button, hide "Activate" button

**How It Works:**
- Called when institute form loads
- Receives current form data (including status)
- Uses `SolidViewLayoutManager` to update layout
- Returns modified layout to UI framework

**Benefits:**
- Prevents invalid actions (can't activate what's already active)
- Clear visual indication of current state
- Follows state machine pattern

### UI Configuration

**Button Configuration in Form View:**

Both buttons are configured as header buttons in the institute form view layout:

**Activate Institute Button:**
```json
{
  "attrs": {
    "label": "Activate Institute",
    "icon": "pi pi-caret-right",
    "action": "InstituteActivateById",
    "customComponentIsSystem": true,
    "actionInContextMenu": true,
    "openInPopup": true,
    "visible": false
  }
}
```

**Deactivate Institute Button:**
```json
{
  "attrs": {
    "label": "Deactivate Institute",
    "icon": "pi pi-circle-off",
    "action": "InstituteDeactivateById",
    "customComponentIsSystem": true,
    "actionInContextMenu": true,
    "openInPopup": true,
    "visible": false
  }
}
```

**Configuration Properties:**
- `action`: References the React component name
- `customComponentIsSystem`: Indicates this is a custom component (not auto-generated)
- `actionInContextMenu`: Shows button in context menu (right-click/three-dot menu)
- `openInPopup`: Opens in a modal dialog
- `visible`: Initially hidden (controlled by edit handler)

### Security Considerations

#### Authentication & Authorization

**Endpoint Security:**
- All activation/deactivation endpoints require JWT authentication
- Bearer token must be included in request headers
- Token validated by NestJS authentication guards

**Role-Based Access Control:**
- Only Platform Admin role can activate/deactivate institutes
- Institute Admins cannot activate their own institute
- Role check enforced at framework level

**Recommended Enhancement:**
Add explicit role guard to controller:
```typescript
@ApiBearerAuth("jwt")
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('Platform Admin')
@Post('activate/:id')
async activateFeePortal(@Param('id') id: number) {
  return this.service.activateInstitutePortal(id);
}
```

#### Infrastructure Security

**Nginx Configuration:**
- Virtual hosts isolated per institute
- No cross-domain access
- Proxy headers sanitized
- HTTP only (upgrade to HTTPS recommended)

**DNS Security:**
- CNAME records validated before creation
- Domain name sanitized (conservative regex)
- TTL set to reasonable value (300s)

**File System Security:**
- Configuration files created with restricted permissions
- Only application service account can modify
- Nginx runs as separate user (www-data)

#### Audit & Compliance

**Audit Trail:**
- All activation/deactivation events logged to Chatter
- Timestamp, user, and action recorded
- Immutable audit log

**Rollback Capability:**
- Deactivation removes infrastructure but preserves data
- Can reactivate institute without data loss
- Configuration history maintained

### Environment Configuration Reference

This section details all environment variables used by the activation system.

#### Required Environment Variables

**PORTAL_CNAME_DOMAIN**
- **Description:** Target domain for CNAME records
- **Required:** Yes
- **Example:** `"portal.solidx.edu"`
- **Used By:** DNS record creation
- **Impact if Missing:** Activation fails with error

#### Optional Environment Variables

**EDU_BASE_DOMAIN**
- **Description:** Base domain for institute subdomains
- **Required:** No
- **Default:** `"solidx.edu"`
- **Example:** `"edu.yourcompany.com"`
- **Used By:** Domain name construction

**DNS_PROVIDER**
- **Description:** DNS management provider
- **Required:** No
- **Default:** `"hosts"`
- **Allowed Values:** `"route53"`, `"hosts"`
- **Example:** `"route53"`
- **Used By:** DNS provider selection

**EDU_FRONTEND_UPSTREAM**
- **Description:** Upstream server for Nginx proxy
- **Required:** No
- **Default:** `"http://127.0.0.1:3002"`
- **Example:** `"http://localhost:3000"`
- **Used By:** Nginx virtual host configuration

#### Route53-Specific Configuration

**AWS Credentials:**
- Can be provided via IAM role (recommended) or environment variables
- Required environment variables:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION` (e.g., `"us-east-1"`)

**Hosted Zone ID:**
- Provided programmatically to Route53WebsiteDnsManager constructor
- Must match the hosted zone for `EDU_BASE_DOMAIN`
- Example: `"Z1234567890ABC"`

#### Example .env Configuration

**Production Setup:**
```bash
# Base configuration
EDU_BASE_DOMAIN=solidx.edu
PORTAL_CNAME_DOMAIN=portal.solidx.edu
DNS_PROVIDER=route53
EDU_FRONTEND_UPSTREAM=http://127.0.0.1:3002

# AWS credentials (or use IAM role)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

**Local Development Setup:**
```bash
# Base configuration
EDU_BASE_DOMAIN=edu.local
PORTAL_CNAME_DOMAIN=portal.local
DNS_PROVIDER=hosts
EDU_FRONTEND_UPSTREAM=http://localhost:3000
```

### Best Practices

#### Before Activation

1. **Validate Configuration**
   - Verify all required institute fields are filled
   - Test payment gateway credentials
   - Confirm support contact information is correct

2. **Plan Domain Name**
   - Choose a clear, memorable hosted page prefix
   - Verify uniqueness before setting
   - Avoid special characters and spaces

3. **Test in Staging**
   - Activate a test institute first
   - Verify DNS resolution
   - Test portal access
   - Check payment flow end-to-end

#### During Activation

1. **Monitor Progress**
   - Watch for success/error messages
   - Check server logs if activation fails
   - Verify each step completes successfully

2. **Document Configuration**
   - Record domain name
   - Note activation date and user
   - Save configuration details

#### After Activation

1. **Verify Infrastructure**
   - Test DNS resolution from multiple locations
   - Check Nginx configuration
   - Verify portal accessibility
   - Test on multiple devices/browsers

2. **Functional Testing**
   - Login as Institute Admin
   - Create a test payment collection
   - Verify student portal loads
   - Test payment flow (in test mode)

3. **Communication**
   - Notify Institute Admin of activation
   - Provide portal URL and credentials
   - Share user documentation
   - Schedule training if needed

4. **Monitoring**
   - Set up uptime monitoring for the domain
   - Monitor server resources (CPU, memory, disk)
   - Check error logs regularly
   - Track payment transaction success rates

#### Operational Best Practices

1. **Backup Before Changes**
   - Backup Nginx configuration before bulk activations
   - Export institute data before major changes
   - Keep DNS records documented

2. **Batch Operations**
   - Activate institutes during low-traffic hours
   - Allow time between activations for verification
   - Limit concurrent activations to avoid resource exhaustion

3. **Documentation**
   - Maintain list of active institutes and domains
   - Document any custom configuration per institute
   - Keep activation dates and responsible admin recorded

4. **Regular Audits**
   - Review active institutes monthly
   - Check for orphaned Nginx configurations
   - Verify DNS records match database status
   - Clean up inactive configurations

### Troubleshooting Reference

#### Common Issues and Solutions

**Issue: Activation button not visible**
- **Cause:** Status is already "Active" or edit handler not working
- **Solution:**
  - Check current status value
  - Verify edit handler is configured in form view
  - Check browser console for JavaScript errors

**Issue: "PORTAL_CNAME_DOMAIN env var not configured" error**
- **Cause:** Missing required environment variable
- **Solution:**
  - Add `PORTAL_CNAME_DOMAIN` to `.env` file
  - Restart API server
  - Verify value with `echo $PORTAL_CNAME_DOMAIN`

**Issue: Nginx reload fails**
- **Cause:** Syntax error in configuration or permission issue
- **Solution:**
  - Run `sudo nginx -t` to check syntax
  - Review generated configuration file
  - Check Nginx error logs: `sudo journalctl -u nginx`
  - Verify application has permission to reload Nginx

**Issue: DNS record not created (Route53)**
- **Cause:** Invalid AWS credentials or wrong hosted zone
- **Solution:**
  - Verify AWS credentials are valid
  - Check hosted zone ID matches `EDU_BASE_DOMAIN`
  - Confirm IAM permissions include `route53:ChangeResourceRecordSets`
  - Check AWS service status

**Issue: Portal returns 502 Bad Gateway**
- **Cause:** Frontend upstream not responding
- **Solution:**
  - Verify frontend service is running
  - Check `EDU_FRONTEND_UPSTREAM` is correct
  - Test upstream directly: `curl http://127.0.0.1:3002`
  - Check frontend logs for errors

**Issue: Portal loads but shows wrong content**
- **Cause:** Frontend routing not matching domain to institute
- **Solution:**
  - Verify `hostedPagePrefix` is unique
  - Check frontend routing logic
  - Clear browser cache
  - Test in incognito/private window

**Issue: Activation succeeds but portal still inaccessible**
- **Cause:** DNS propagation delay or browser cache
- **Solution:**
  - Wait 10-15 minutes for DNS propagation
  - Flush local DNS cache
  - Test from different network/location
  - Use `nslookup` or `dig` to verify DNS

**Issue: Cannot deactivate institute**
- **Cause:** Permission issue or configuration locked
- **Solution:**
  - Verify you're logged in as Platform Admin
  - Check if there are active payment collections
  - Review server logs for specific error
  - Try deactivating from API directly (debugging)

#### Diagnostic Commands

**Check DNS Resolution:**
```bash
# Using nslookup
nslookup stmary.solidx.edu

# Using dig
dig stmary.solidx.edu

# Check CNAME specifically
dig CNAME stmary.solidx.edu
```

**Check Nginx Configuration:**
```bash
# Test configuration syntax
sudo nginx -t

# View configuration
cat /etc/nginx/sites-available/stmary.solidx.edu.conf

# Check if symlink exists
ls -la /etc/nginx/sites-enabled/ | grep stmary

# Reload Nginx
sudo systemctl reload nginx

# Check Nginx status
sudo systemctl status nginx
```

**Check Application Logs:**
```bash
# PM2 logs
pm2 logs solid-api --lines 100

# Direct log files
tail -f /var/log/solid-api/error.log
tail -f /var/log/solid-api/combined.log
```

**Check Hosts File (Local):**
```bash
# View hosts file
cat /etc/hosts

# Search for specific domain
cat /etc/hosts | grep stmary

# Check file permissions
ls -la /etc/hosts
```

**Test Portal Access:**
```bash
# Simple GET request
curl -I http://stmary.solidx.edu

# Full response
curl http://stmary.solidx.edu

# With verbose output
curl -v http://stmary.solidx.edu

# Follow redirects
curl -L http://stmary.solidx.edu
```

### Success Criteria

You've successfully activated an institute when:

- [ ] Status field shows "Active" in database and UI
- [ ] "Activate Institute" button is hidden
- [ ] "Deactivate Institute" button is visible
- [ ] Nginx configuration file exists in sites-available
- [ ] Symlink exists in sites-enabled
- [ ] DNS CNAME record created and resolving
- [ ] Portal accessible at `http://{hostedPagePrefix}-{EDU_BASE_DOMAIN}`
- [ ] Portal loads without errors
- [ ] Institute branding appears correctly
- [ ] Student portal login page accessible
- [ ] Audit trail entry created in Chatter
- [ ] Institute Admin notified of activation

### Related Documentation

- [Institute Onboarding](./institute_onboarding.md) - Complete guide to onboarding new institutes
- [Initiate Payment Collection](./initiate_payment.md) - How to create payment collections after activation
- [User Roles & Responsibilities](./fees_portal_product_overview#user-roles--responsibilities) - Understanding platform roles

### Frequently Asked Questions

**Q: Can I activate multiple institutes at once?**
A: No, activation must be done one institute at a time through the UI. Bulk activation would require a custom script using the API endpoints.

**Q: How long does activation take?**
A: Typically 5-30 seconds for infrastructure provisioning. DNS propagation can take 5-15 minutes depending on your provider and TTL settings.

**Q: Can I change the domain after activation?**
A: No, the domain is based on `hostedPagePrefix` which cannot be changed after activation. You would need to deactivate, change the prefix, and reactivate.

**Q: What happens to data when I deactivate?**
A: All data (students, payments, configuration) remains in the database. Only the infrastructure (Nginx config and DNS) is removed. Reactivating restores access to the same data.

**Q: Can Institute Admins activate their own institute?**
A: No, only Platform Admins have permission to activate/deactivate institutes.

**Q: What if activation fails halfway through?**
A: The system attempts to maintain consistency, but partial failures can occur. Check server logs, clean up manually if needed (remove Nginx config/DNS record), then try again.

**Q: Do I need HTTPS/SSL certificates?**
A: The basic activation creates HTTP configuration. For production, you should configure SSL/TLS certificates (Let's Encrypt recommended) separately.

**Q: Can I use a custom domain instead of subdomain?**
A: The current implementation uses subdomains only. Custom domain support would require code modifications to the DNS and Nginx providers.

**Q: How many institutes can I activate?**
A: No hard limit, but consider server resources (Nginx can handle thousands of virtual hosts) and DNS provider limits.

**Q: What are the server requirements for 100 active institutes?**
A: Nginx overhead is minimal. Main consideration is application server resources. Monitor CPU/memory usage and scale horizontally if needed.

---

**This completes the Activate Institute guide. For questions or issues not covered here, contact the platform development team.**