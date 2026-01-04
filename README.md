# Auctions - E-Commerce Auction Platform

A modern, minimalist e-commerce auction platform built with Django, featuring real-time bidding, watchlists, and category-based browsing.

![Auctions Platform](https://img.shields.io/badge/Django-5.2-green)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

## 📋 Overview

Auctions is a full-featured online auction platform that allows users to create listings, place bids, add items to watchlists, and engage with the community through comments. Built with a clean, Apple-inspired minimalist design philosophy.

## ✨ Features

### Core Functionality
- **User Authentication** - Secure registration, login, and session management
- **Create Listings** - Post auction items with images, descriptions, and starting prices
- **Real-time Bidding** - Place bids with automatic validation and price updates
- **Watchlist** - Save favorite items and track your bidding activity
- **Categories** - Browse items by category (Electronics, Fashion, Home, etc.)
- **Comments** - Engage with listings through a comment system
- **Auction Management** - Sellers can close auctions and declare winners

### Design Features
- Clean, minimalist UI inspired by Apple's design language
- Fully responsive layout for mobile, tablet, and desktop
- Smooth shadows and white space for visual hierarchy
- Intuitive navigation and user experience

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/CapBraco/auctions-list.git
cd auctions-list
```

2. **Create and activate virtual environment**
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations auctions
python manage.py migrate
```

5. **Create a superuser (admin account)**
```bash
python manage.py createsuperuser
```

6. **Start the development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Open your browser and navigate to `http://127.0.0.1:8000`
- Admin interface available at `http://127.0.0.1:8000/admin`

## 📱 Usage

### For Buyers
1. **Register/Login** - Create an account or sign in
2. **Browse Listings** - View active auctions on the homepage
3. **Filter by Category** - Navigate to specific categories
4. **Place Bids** - Enter your bid amount (must exceed current price)
5. **Add to Watchlist** - Save items you're interested in
6. **Track Your Bids** - Monitor your bidding activity in "My Watchlist"
7. **Comment** - Engage with sellers and other bidders

### For Sellers
1. **Create Listing** - Click "Create Auction"
2. **Add Details** - Provide title, description, image, and category
3. **Set Starting Price** - Define the minimum bid and end time
4. **Manage Auction** - Update status or close the auction
5. **Complete Sale** - System automatically records the winner

## 🗂️ Project Structure

```
commerce/
├── auctions/               # Main application directory
│   ├── migrations/        # Database migrations
│   ├── static/           # Static files (CSS, JS, images)
│   ├── templates/        # HTML templates
│   ├── admin.py          # Admin configuration
│   ├── forms.py          # Django forms
│   ├── models.py         # Database models
│   ├── urls.py           # URL routing
│   └── views.py          # View functions
├── commerce/              # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py           # WSGI configuration
├── media/                # User-uploaded files
├── staticfiles/          # Collected static files
├── db.sqlite3           # SQLite database
└── manage.py            # Django management script
```

## 💾 Database Models

### User
Extended Django's AbstractUser model for authentication

### Product
- Fields: name, description, long_description, image, categories
- Relationships: belongs to User, has many Categories

### Auction
- Fields: starting_price, current_price, status, start/end times
- Relationships: one-to-one with Product

### Bid
- Fields: amount, created_at
- Relationships: belongs to Auction and User

### Comment
- Fields: comment, created_at
- Relationships: belongs to Product and User

### Category
- Fields: name
- Relationships: many-to-many with Products

### Like (Watchlist)
- Relationships: belongs to User and Product

### Transaction
- Fields: final_price, completed_at
- Relationships: connects buyer, seller, and auction

## 🎨 Design Philosophy

The UI embraces minimalism with:
- **White space** - Generous padding and margins
- **Subtle shadows** - Depth without clutter
- **Clean typography** - Clear hierarchy and readability
- **Responsive grid** - Adapts seamlessly to all screen sizes
- **Intuitive navigation** - Easy access to core features

## 🛠️ Technologies Used

- **Backend**: Django 5.2
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development)
- **Authentication**: Django Auth
- **Forms**: Django Forms with custom styling
- **Static Files**: Django Static Files

## 📊 Admin Features

Access the Django admin panel to:
- Manage users, products, and auctions
- View and moderate comments
- Track bids and transactions
- Manage categories
- Monitor platform activity

## 🔒 Security Features

- CSRF protection on all forms
- Password hashing
- Login required decorators for protected views
- User authentication and session management
- Input validation and sanitization

## 🚧 Future Enhancements

- [ ] Real-time notifications for outbid alerts
- [ ] Advanced search and filtering
- [ ] User ratings and reviews
- [ ] Payment integration
- [ ] Email notifications
- [ ] Auction timer countdown
- [ ] Image gallery for products
- [ ] PostgreSQL for production
- [ ] API endpoints for mobile app

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Built as part of CS50's Web Programming with Python and JavaScript course.

## 🙏 Acknowledgments

- CS50 Web Programming course
- Django documentation
- Bootstrap framework
- The open-source community

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This is a educational project and should not be used in production without proper security hardening, testing, and scaling considerations.