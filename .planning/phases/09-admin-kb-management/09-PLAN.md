# Phase 9: Admin — KB Management - Implementation Plan

> **For Antigravity:** REQUIRED SUB-SKILL: Load `executing-plans` to implement this plan task-by-task.

**Goal:** Backend admin endpoints for Qdrant collection management + frontend admin dashboard with drag-and-drop PDF upload.

**Design:** Data-Dense Dashboard style — row highlighting, hover tooltips, status badges. Uses UUPM OLED dark theme from MASTER.md.

---

## Verification Plan
- Backend: `PYTHONPATH=$PWD poetry run pytest -v` must pass after Task 1.
- Frontend: `cd frontend && npm run test` must pass after each task.

### Task 1: Backend Admin API Endpoints

**Files:**
- Modify: `src/main.py` (add 3 admin routes)
- Test: `tests/test_api.py` (add admin endpoint tests)

<acceptance_criteria>
- `GET /admin/kb` returns list of KBs: `[{name, agent_id, document_count}]`.
- `GET /admin/kb/{agent_id}` returns collection details: `{name, agent_id, document_count, vector_size}`.
- `DELETE /admin/kb/{agent_id}` deletes the Qdrant collection, returns `{status: "deleted"}`.
- All admin endpoints require auth (`Depends(get_current_user)`).
- 404 returned when collection doesn't exist.
</acceptance_criteria>

**Step 1: Write failing tests**
```python
def test_list_kb_returns_collections(client): ...
def test_get_kb_details(client): ...
def test_delete_kb(client): ...
def test_admin_endpoints_require_auth(client): ...
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(09): add admin KB management API endpoints"`

---

### Task 2: Admin Layout & Router Update

**Files:**
- Create: `frontend/src/layouts/AdminLayout.vue`
- Create: `frontend/src/components/AdminTopNav.vue`
- Modify: `frontend/src/router/index.js` (add admin sub-routes)
- Modify: `frontend/src/views/admin/DashboardView.vue`

<acceptance_criteria>
- `AdminLayout.vue` wraps admin pages with `AdminTopNav`.
- `AdminTopNav` has tabs: "Knowledge Bases" (active), "Chatbots" (Phase 10).
- Router: `/admin` → redirects to `/admin/kb`. `/admin/kb` renders KB dashboard.
- Admin layout uses dark theme, data-focused styling.
</acceptance_criteria>

**Step 1: Write minimal implementation**

**Step 2: Commit**
`git commit -m "feat(09): add admin layout with top navigation"`

---

### Task 3: KB Dashboard Page

**Files:**
- Create: `frontend/src/views/admin/KBListView.vue`
- Create: `frontend/src/composables/useKnowledgeBases.js`
- Test: `frontend/src/composables/__tests__/useKnowledgeBases.test.js`

<acceptance_criteria>
- `useKnowledgeBases()` returns reactive `kbs`, `isLoading`, `fetchKBs()`, `deleteKB()`.
- `KBListView.vue` displays a table/grid of knowledge bases with name, document count, and actions.
- Each KB row has a "Delete" button with confirmation dialog.
- Empty state shown when no KBs exist.
- Status badges for document count (green for >0, gray for empty).
</acceptance_criteria>

**Step 1: Write failing tests**
```js
describe('useKnowledgeBases', () => {
  it('fetches KB list from API', async () => { ... })
  it('deletes a KB', async () => { ... })
})
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(09): add KB dashboard with list and delete"`

---

### Task 4: File Upload Component

**Files:**
- Create: `frontend/src/components/FileUploadZone.vue`
- Test: `frontend/src/components/__tests__/FileUploadZone.test.js`

<acceptance_criteria>
- Drag-and-drop zone accepts PDF files.
- Click-to-browse file picker as fallback.
- Accepts multiple files, filters to `.pdf` only.
- Displays upload progress per file (uploading / done / error).
- Each file calls `POST /ingest` with the selected `agent_id`.
- Upload zone integrated into `KBListView.vue` with an agent_id selector.
</acceptance_criteria>

**Step 1: Write failing tests**
```js
describe('FileUploadZone', () => {
  it('renders drop zone with instructions', () => { ... })
  it('filters non-PDF files', () => { ... })
})
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(09): add drag-and-drop file upload component"`
