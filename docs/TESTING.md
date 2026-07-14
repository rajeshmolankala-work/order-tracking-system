# Testing Guide - Order Tracking System

## Manual Testing Checklist

This document provides a comprehensive testing guide for all features of the Order Tracking System.

---

## 1. Authentication Testing

### Login Page
- [ ] Login page loads correctly
- [ ] Login form displays all fields
- [ ] Can login with correct credentials (admin/admin123)
- [ ] Error message appears with incorrect credentials
- [ ] Password field masks input
- [ ] Login button is clickable
- [ ] Demo credentials are displayed

### Session Management
- [ ] Session persists when navigating between pages
- [ ] Session expires after logout
- [ ] Accessing protected pages without login redirects to login
- [ ] Logout clears session data
- [ ] User info displays in navbar after login

---

## 2. Dashboard Testing

### Dashboard Load
- [ ] Dashboard loads without errors
- [ ] All stat cards display correct counts
- [ ] Recent orders table shows data
- [ ] Total revenue is calculated correctly
- [ ] Status distribution is accurate

### Dashboard Navigation
- [ ] "Add New Order" button navigates to add order page
- [ ] "View All Orders" button navigates to orders list
- [ ] "Generate Reports" button navigates to reports page
- [ ] Navigation links work properly

---

## 3. Order Management Testing

### Add Order
- [ ] Add order page loads correctly
- [ ] All form fields are present
- [ ] Form validation works:
  - [ ] Order ID validation (3-20 chars, alphanumeric + hyphens)
  - [ ] Customer name validation (2-100 chars)
  - [ ] Product name validation
  - [ ] Quantity validation (must be > 0)
  - [ ] Price validation (cannot be negative)
  - [ ] Order date validation (YYYY-MM-DD format)
  - [ ] Delivery date validation
  - [ ] Contact number validation
  - [ ] Shipping address validation (5-250 chars)
  
- [ ] Duplicate Order ID prevention works
- [ ] Success message appears after adding
- [ ] Order appears in orders list
- [ ] Status is recorded in history

### View Orders
- [ ] Orders list loads without errors
- [ ] All columns display correctly
- [ ] Pagination works (10 items per page)
- [ ] Previous/Next buttons work
- [ ] Order count is accurate
- [ ] Status badges show correct colors
- [ ] Payment status badges display correctly
- [ ] View button opens order details
- [ ] Edit button opens edit form
- [ ] Delete button shows confirmation

### Order Details
- [ ] All order information displays correctly
- [ ] Status history timeline shows all changes
- [ ] Timeline items have correct timestamps
- [ ] Status update form is present
- [ ] Status dropdown has all 7 options
- [ ] Edit button works
- [ ] Delete button shows confirmation

### Edit Order
- [ ] Edit form pre-fills all data
- [ ] Order ID field is disabled (cannot edit)
- [ ] Can update customer name
- [ ] Can update product details
- [ ] Can update quantity and price
- [ ] Can update delivery date
- [ ] Can update status
- [ ] Can update payment status
- [ ] Can update tracking number
- [ ] Can update shipping address
- [ ] Can update contact number
- [ ] Success message appears after update
- [ ] Status change is recorded in history

### Delete Order
- [ ] Confirmation dialog appears
- [ ] Can cancel deletion
- [ ] Order is deleted after confirmation
- [ ] Order disappears from list
- [ ] Status history is also deleted
- [ ] Success message appears

---

## 4. Search Testing

### Search Functionality
- [ ] Search page loads correctly
- [ ] All search types available:
  - [ ] Order ID
  - [ ] Customer Name
  - [ ] Product Name
  - [ ] Tracking Number
  - [ ] Status
  
- [ ] Empty search shows error
- [ ] Search results display correctly
- [ ] Result count is accurate
- [ ] Can click "View" to see order details
- [ ] Case-insensitive search works
- [ ] Partial matching works
- [ ] No results shows appropriate message

---

## 5. Status Management Testing

### Status Update
- [ ] Can update status from order details page
- [ ] Status dropdown shows all 7 options
- [ ] Current status is not available in dropdown
- [ ] Status updates without page reload
- [ ] Confirmation message appears
- [ ] Status changes in real-time
- [ ] History is updated with timestamp

### Status Tracking
- [ ] Initial status is recorded when order is created
- [ ] Status history shows all changes
- [ ] Each change has correct old and new status
- [ ] Timestamps are accurate
- [ ] Status badges update color based on status

---

## 6. Reports Testing

### Report Generation
- [ ] Reports page loads correctly
- [ ] Report type dropdown has all options
- [ ] Date range selection works
- [ ] Can generate daily report
- [ ] Can generate weekly report
- [ ] Can generate monthly report
- [ ] Date validation prevents invalid ranges
- [ ] Error message for start date > end date

### Report Display
- [ ] Report statistics display correctly
- [ ] Total orders count is accurate
- [ ] Pending orders count is accurate
- [ ] Delivered orders count is accurate
- [ ] Cancelled orders count is accurate
- [ ] Total revenue is calculated correctly
- [ ] Orders table displays all data

### Export from Reports
- [ ] Excel export button visible
- [ ] CSV export button visible
- [ ] Date range is preserved in export
- [ ] Report type affects export data

---

## 7. Export Testing

### Excel Export
- [ ] Excel file downloads correctly
- [ ] File format is .xlsx
- [ ] File has correct name with timestamp
- [ ] File saves in exports folder
- [ ] Headers are formatted (bold, colored)
- [ ] All columns are present
- [ ] Column widths are appropriate
- [ ] Data is formatted correctly
- [ ] Total amounts are calculated correctly
- [ ] Can export all orders
- [ ] Can export by date range
- [ ] Can export pending orders
- [ ] Can export delivered orders

### CSV Export
- [ ] CSV file downloads correctly
- [ ] File format is .csv
- [ ] File has correct name with timestamp
- [ ] File saves in exports folder
- [ ] Headers are included
- [ ] All columns are present
- [ ] Data is properly separated by commas
- [ ] Can open in Excel
- [ ] Can open in Google Sheets
- [ ] Can export all orders
- [ ] Can export by date range
- [ ] Can export pending orders
- [ ] Can export delivered orders

---

## 8. UI/UX Testing

### Navigation Bar
- [ ] Navbar is sticky (stays at top)
- [ ] All menu items are visible
- [ ] All menu items are clickable
- [ ] Username displays correctly
- [ ] Logout button works
- [ ] Navigation responsive on mobile

### Responsive Design
#### Desktop (1024px+)
- [ ] All elements display correctly
- [ ] Tables are fully visible
- [ ] Forms are properly formatted
- [ ] Navigation is horizontal

#### Tablet (768px - 1023px)
- [ ] Layout adjusts properly
- [ ] No horizontal scroll needed
- [ ] Touch buttons are appropriately sized
- [ ] Tables remain readable

#### Mobile (< 768px)
- [ ] Layout is vertical
- [ ] Navigation is accessible
- [ ] Forms are easy to fill
- [ ] Buttons are touch-friendly
- [ ] No horizontal scrolling

### Alerts & Messages
- [ ] Success alerts display and auto-hide
- [ ] Error alerts display and auto-hide
- [ ] Info alerts display and auto-hide
- [ ] Alert colors are correct
- [ ] Close button works on alerts

---

## 9. Data Validation Testing

### Client-Side Validation
- [ ] Required fields prevent submission
- [ ] Number fields reject letters
- [ ] Email-like fields validate format
- [ ] Date fields validate format
- [ ] Length validations work

### Server-Side Validation
- [ ] Invalid data is rejected at server
- [ ] Error messages are informative
- [ ] No data is saved if validation fails
- [ ] SQL injection attempts are prevented

---

## 10. Performance Testing

### Page Load Times
- [ ] Dashboard loads in < 2 seconds
- [ ] Orders list loads in < 2 seconds
- [ ] Search results load in < 1 second
- [ ] Reports generate in < 3 seconds

### Database Performance
- [ ] Large datasets paginate smoothly
- [ ] Searches are fast
- [ ] Exports complete quickly

---

## 11. Security Testing

### Authentication
- [ ] Cannot access protected pages without login
- [ ] Cannot access other user's data
- [ ] Session timeout works
- [ ] CSRF tokens are validated

### Data Protection
- [ ] Passwords are not displayed in plain text
- [ ] Sensitive data is not logged
- [ ] Database backups are secure

---

## 12. Browser Compatibility Testing

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers

---

## Test Data

### Sample Orders for Testing
