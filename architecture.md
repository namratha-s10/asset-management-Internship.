# OptiAsset Frontend Architecture Mapping

## Role: IT Administrator (Full Access)
### Page: /dashboard (Overview)
- Component: <Sidebar /> - Navigation links.
- Component: <StatCards /> - Shows Total, Deployed, and Broken Assets.
- Component: <RecentActivity /> - List of latest asset assignments.

### Page: /inventory (Management)
- Component: <InventoryTable /> - Searchable list of all hardware.
- Component: <AddAssetModal /> - Form to add new devices to the DB.

## Role: Standard Employee (Limited View)
### Page: /my-gear (Personal Portal)
- Component: <TopNavbar /> - Profile and Logout button.
- Component: <MyAssetCard /> - Details of hardware assigned to the user.
- Component: <ReportIssueButton /> - Opens a form to report damage.