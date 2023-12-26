# Home-Services-Booking-App
With a home service application, sellers can register their services, and customers can easily book and avail them. Services such as cleaning, electrician, plumbing, paint, and more are available. An admin can approve or reject newly added service by sellers, and customers can review and rate their experiences after availing a service.

## Project Requirements
### About:
With a home service application, sellers can register their services, and customers can easily book and avail them. Services such as cleaning, electrician, plumbing, paint, and more are available. An admin can approve or reject newly added service by sellers, and customers can review and rate their experiences after availing a service. 
Furthermore, a single seller can add multiple services and customers can avail multiple services simultaneously

### Registration and Authorization:
#### User can be a: 
- Customer
- Seller (Service Provider)
- Admin

#### User should be able to:
- Register(name, gender, age, mail, password, role[seller, customer])
- Login [email, password]
- Confirm email 
- On 5 incorrect attempts login should be disabled for 5 minutes
- Admin will be added by default

### Customer Dashboard:
Customer will be able to:
- View all available services
- Sort available services on basis of date
- Search services by category
- View individual service detail 
- Can book a service
- Rating
- Payment (Use Stripe for this)
- View on-going services
- View completed services
- Can rate and review service
Note: Use pagination where required

### Admin Dashboard:
Admin can:
- Manage categories for service
- Add category
- Delete category 
- View all newly added services
- Approve a new service 
- Reject a new service
- Can give a reason for rejection
- View list of all approved services
- View list of all rejected services
- View rejected service and approve them

### Seller Dashboard:
Seller can
- View all of his / her services
- Each service will display its status( pending / approved / rejected)
- In case of reject status, seller can resolve admin comments and can request for re-approval
- Registration new service
- View all reviews submitted for individual service

Note: Use pagination where required
