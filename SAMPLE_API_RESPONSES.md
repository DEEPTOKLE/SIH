# IP-SAKTI Dashboard - Sample API Responses

Use these sample responses for demo purposes, documentation, and frontend development without a running backend.

## 1. Authentication Response

```json
POST /api/auth/token/
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## 2. Dashboard KPIs Response

```json
GET /api/dashboard/kpis/
{
  "total_gi_tags": 342,
  "total_patents": 567,
  "total_biopiracy_alerts": 89,
  "active_biopiracy_cases": 23,
  "resolved_biopiracy_cases": 66,
  "texts_digitized": 4750,
  "total_formulations": 215,
  "registered_formulations": 189,
  "india_prior_art_success": 67,
  "monthly_trends": {
    "2024-01": { "gi_tags": 12, "patents": 25, "biopiracy_cases": 5 },
    "2024-02": { "gi_tags": 15, "patents": 30, "biopiracy_cases": 3 },
    "2024-03": { "gi_tags": 18, "patents": 22, "biopiracy_cases": 8 },
    "2024-04": { "gi_tags": 20, "patents": 28, "biopiracy_cases": 6 },
    "2024-05": { "gi_tags": 25, "patents": 35, "biopiracy_cases": 4 },
    "2024-06": { "gi_tags": 22, "patents": 40, "biopiracy_cases": 7 },
    "2024-07": { "gi_tags": 28, "patents": 45, "biopiracy_cases": 9 },
    "2024-08": { "gi_tags": 30, "patents": 38, "biopiracy_cases": 5 },
    "2024-09": { "gi_tags": 35, "patents": 50, "biopiracy_cases": 6 },
    "2024-10": { "gi_tags": 32, "patents": 48, "biopiracy_cases": 8 },
    "2024-11": { "gi_tags": 38, "patents": 55, "biopiracy_cases": 10 },
    "2024-12": { "gi_tags": 40, "patents": 60, "biopiracy_cases": 12 }
  },
  "category_distribution": {
    "AYURVEDA": { "gi_tags": 180, "patents": 320, "formulations": 120 },
    "YOGA": { "gi_tags": 45, "patents": 85, "formulations": 35 },
    "UNANI": { "gi_tags": 35, "patents": 60, "formulations": 25 },
    "SIDDHA": { "gi_tags": 30, "patents": 45, "formulations": 20 },
    "HOMOEOPATHY": { "gi_tags": 40, "patents": 50, "formulations": 15 },
    "SOWRIGANDHA": { "gi_tags": 12, "patents": 7, "formulations": 0 }
  },
  "state_wise_data": [
    {
      "state_id": "550e8400-e29b-41d4-a716-446655440000",
      "state_name": "Kerala",
      "state_code": "KL",
      "latitude": 10.8505,
      "longitude": 76.2711,
      "gi_tags": 45,
      "patents": 0,
      "formulations": 32,
      "biopiracy_cases": 8
    },
    {
      "state_id": "550e8400-e29b-41d4-a716-446655440001",
      "state_name": "Tamil Nadu",
      "state_code": "TN",
      "latitude": 11.1271,
      "longitude": 78.6569,
      "gi_tags": 52,
      "patents": 0,
      "formulations": 45,
      "biopiracy_cases": 12
    },
    {
      "state_id": "550e8400-e29b-41d4-a716-446655440002",
      "state_name": "Karnataka",
      "state_code": "KA",
      "latitude": 15.3173,
      "longitude": 75.7139,
      "gi_tags": 38,
      "patents": 0,
      "formulations": 28,
      "biopiracy_cases": 6
    },
    {
      "state_id": "550e8400-e29b-41d4-a716-446655440003",
      "state_name": "Maharashtra",
      "state_code": "MH",
      "latitude": 19.7515,
      "longitude": 75.7139,
      "gi_tags": 41,
      "patents": 0,
      "formulations": 22,
      "biopiracy_cases": 9
    },
    {
      "state_id": "550e8400-e29b-41d4-a716-446655440004",
      "state_name": "West Bengal",
      "state_code": "WB",
      "latitude": 22.9868,
      "longitude": 87.8550,
      "gi_tags": 35,
      "patents": 0,
      "formulations": 18,
      "biopiracy_cases": 5
    }
  ],
  "recent_alerts": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "type": "BIOPIRACY",
      "type_display": "Biopiracy Alert",
      "severity": "CRITICAL",
      "severity_display": "Critical",
      "title": "LIVE: Biopiracy Alert - Chinese patent on Ashwagandha extract formulation",
      "message": "New biopiracy attempt detected from China. Risk score: 95. TKDL prior art identified. Immediate action required.",
      "related_case": "770e8400-e29b-41d4-a716-446655440000",
      "is_read": false,
      "is_action_required": true,
      "created_at": "2026-09-10T13:30:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "type": "BIOPIRACY",
      "type_display": "Biopiracy Alert",
      "severity": "HIGH",
      "severity_display": "High",
      "title": "Japanese patent filing on traditional Shilajit composition",
      "message": "Japan patent office filing detected on Shilajit extract. Prior art from Charaka Samhita available.",
      "related_case": "770e8400-e29b-41d4-a716-446655440001",
      "is_read": false,
      "is_action_required": true,
      "created_at": "2026-09-10T12:15:00Z"
    }
  ],
  "recent_activities": [
    {
      "id": "880e8400-e29b-41d4-a716-446655440000",
      "activity_type": "BIOPIRACY_RESOLVED",
      "activity_type_display": "Biopiracy Resolved",
      "title": "US Patent revoked: Turmeric wound healing case",
      "description": "Successfully challenged US Patent USPTO 5,401,504 using TKDL prior art. Patent revoked.",
      "related_state": null,
      "related_state_name": null,
      "metadata": { "case_id": "770e8400-e29b-41d4-a716-446655440002", "patent_id": "990e8400-e29b-41d4-a716-446655440000" },
      "created_at": "2026-09-09T18:00:00Z"
    },
    {
      "id": "880e8400-e29b-41d4-a716-446655440001",
      "activity_type": "GI_ISSUED",
      "activity_type_display": "GI Tag Issued",
      "title": "GI Tag issued for Coimbatore Wet Grinder",
      "description": "GI registration number GI-007 issued to Tamil Nadu Industries",
      "related_state_name": "Tamil Nadu",
      "created_at": "2026-09-09T14:30:00Z"
    }
  ]
}
```

## 3. Biopiracy Cases Response

```json
GET /api/biopiracy-cases/
{
  "count": 45,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440000",
      "patent": {
        "id": "990e8400-e29b-41d4-a716-446655440000",
        "title": "Chinese patent on Ashwagandha extract for immunomodulation",
        "applicant": "Guangzhou Herbal Technologies Co. Ltd.",
        "country": "CN",
        "filing_date": "2026-08-15"
      },
      "formulation": {
        "id": "aa0e8400-e29b-41d4-a716-446655440000",
        "name": "Ashwagandha Rasayana",
        "category": "AYURVEDA"
      },
      "status": "DETECTED",
      "status_display": "Detected",
      "priority": "CRITICAL",
      "priority_display": "Critical",
      "detected_date": "2026-09-10T13:30:00Z",
      "risk_score": 95,
      "description": "Automated detection: Non-Indian applicant filing on traditional Ashwagandha formulation without TKDL citation",
      "assigned_to": null,
      "assigned_to_name": null,
      "prior_art_submitted": false,
      "country_of_origin": "China"
    },
    {
      "id": "770e8400-e29b-41d4-a716-446655440001",
      "patent": {
        "id": "990e8400-e29b-41d4-a716-446655440001",
        "title": "Japanese formulation for Shilajit extract standardization",
        "applicant": "Tokyo Herbal Research Institute",
        "country": "JP",
        "filing_date": "2026-09-01"
      },
      "formulation": {
        "id": "aa0e8400-e29b-41d4-a716-446655440001",
        "name": "Shilajit Satva",
        "category": "AYURVEDA"
      },
      "status": "UNDER_REVIEW",
      "status_display": "Under Review",
      "priority": "HIGH",
      "priority_display": "High",
      "detected_date": "2026-09-05T10:00:00Z",
      "risk_score": 85,
      "description": "Potential biopiracy on Shilajit formulation. Risk factors: Non-Indian applicant; TKDL match found",
      "assigned_to": {
        "id": "110e8400-e29b-41d4-a716-446655440000",
        "first_name": "Arun",
        "last_name": "Verma"
      },
      "assigned_to_name": "Arun Verma",
      "prior_art_submitted": false,
      "country_of_origin": "Japan"
    }
  ]
}
```

## 4. Alerts Response

```json
GET /api/alerts/
{
  "count": 89,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "type": "BIOPIRACY",
      "type_display": "Biopiracy Alert",
      "severity": "CRITICAL",
      "severity_display": "Critical",
      "title": "LIVE: Biopiracy Alert - Chinese patent on Ashwagandha",
      "message": "Patent filed by Chinese company on traditional Ashwagandha formulation without prior art citation. Risk score: 95.",
      "is_read": false,
      "is_action_required": true,
      "created_at": "2026-09-10T13:30:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "type": "PATENT",
      "type_display": "Patent Alert",
      "severity": "MEDIUM",
      "severity_display": "Medium",
      "title": "New patent filed: Ayurvedic sleep aid",
      "message": "New patent application filed for Ayurvedic sleep aid formulation by Zandu Pharmaceuticals",
      "is_read": true,
      "is_action_required": false,
      "created_at": "2026-09-10T11:00:00Z"
    }
  ]
}
```

## 5. GI Tags Response

```json
GET /api/gi-tags/
{
  "count": 342,
  "results": [
    {
      "id": "aa0e8400-e29b-41d4-a716-446655440000",
      "name": "Darjeeling Tea",
      "product": "Tea",
      "description": "World-famous tea from Darjeeling region",
      "state": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "West Bengal",
        "code": "WB"
      },
      "category": "AYURVEDA",
      "status": "REGISTERED",
      "status_display": "Registered",
      "issued_date": "2005-10-20",
      "applicant": "Tea Board India",
      "registration_number": "GI-001",
      "is_ayush_related": true
    },
    {
      "id": "aa0e8400-e29b-41d4-a716-446655440001",
      "name": "Basmati Rice",
      "product": "Rice",
      "description": "Aromatic long-grain rice from Himalayan foothills",
      "state": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Punjab",
        "code": "PB"
      },
      "category": "AYURVEDA",
      "status": "REGISTERED",
      "status_display": "Registered",
      "issued_date": "2016-02-15",
      "applicant": "APEDA",
      "registration_number": "GI-002",
      "is_ayush_related": true
    }
  ]
}
```

## 6. Patents Response

```json
GET /api/patents/
{
  "count": 567,
  "results": [
    {
      "id": "990e8400-e29b-41d4-a716-446655440000",
      "title": "Novel Ayurvedic Formulation for Diabetes Management",
      "applicant": "CSIR-IMTECH",
      "country": "IN",
      "application_number": "IN/2024/12345",
      "filing_date": "2019-05-15",
      "status": "GRANTED",
      "status_display": "Granted",
      "ayush_category": "AYURVEDA",
      "ayush_category_display": "Ayurveda",
      "is_biopiracy_suspect": false,
      "biopiracy_risk_score": 0,
      "assignee": "CSIR-IMTECH",
      "inventors": "Dr. R. Kumar, Dr. S. Sharma"
    }
  ]
}
```

## 7. State-wise Analytics Response

```json
GET /api/dashboard/state-analytics/?state_id=550e8400-e29b-41d4-a716-446655440000
{
  "state": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Kerala",
    "code": "KL",
    "region": "SOUTH",
    "ayush_council_name": "Kerala State AYUSH Society",
    "population": 35000000,
    "latitude": 10.8505,
    "longitude": 76.2711
  },
  "gi_tags": 45,
  "patents": 12,
  "formulations": 32,
  "biopiracy_cases": 8,
  "tkdl_coverage": 95.5
}
```

## 8. Alerts Unread Count Response

```json
GET /api/alerts/unread-count/
{
  "unread_count": 5
}
```

## 9. Biopiracy Cases Dashboard Summary

```json
GET /api/biopiracy-cases/dashboard_summary/
{
  "total_cases": 45,
  "by_status": {
    "DETECTED": 12,
    "UNDER_REVIEW": 8,
    "ESCALATED": 5,
    "PRIOR_ART_FILED": 15,
    "RESOLVED": 5
  },
  "by_priority": {
    "LOW": 8,
    "MEDIUM": 15,
    "HIGH": 15,
    "CRITICAL": 7
  },
  "recent_cases": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440000",
      "patent_title": "Chinese patent on Ashwagandha extract",
      "status": "DETECTED",
      "priority": "CRITICAL",
      "detected_date": "2026-09-10T13:30:00Z"
    }
  ],
  "assigned_to_me": 2
}
```

---

## Using Sample Data in Frontend

For demo purposes, you can create a mock API service:

```javascript
// src/services/mockApi.js
export const mockKPIs = {
  total_gi_tags: 342,
  total_patents: 567,
  total_biopiracy_alerts: 89,
  active_biopiracy_cases: 23,
  resolved_biopiracy_cases: 66,
  texts_digitized: 4750,
  total_formulations: 215,
  registered_formulations: 189,
  india_prior_art_success: 67,
  monthly_trends: { /* ... */ },
  category_distribution: { /* ... */ },
  state_wise_data: [ /* ... */ ],
};

export const mockAlerts = [
  {
    id: '1',
    type: 'BIOPIRACY',
    severity: 'CRITICAL',
    title: 'Chinese patent on Ashwagandha',
    message: '...',
    is_read: false,
    created_at: '2026-09-10T13:30:00Z',
  }
];

// Use in development
const useMockData = true;
export const api = useMockData ? mockApi : realApi;
```

---

*These sample responses can be used for:*
- *Frontend development without backend*
- *Demo presentations*
- *Documentation*
- *Testing*
