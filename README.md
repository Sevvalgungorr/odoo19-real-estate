# Real Estate Management — Odoo 19 Module

![Odoo](https://img.shields.io/badge/Odoo-19.0-714B67?logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-backend-4169E1?logo=postgresql&logoColor=white)

A custom Odoo 19 module for managing real estate listings, buyer offers and the sales lifecycle.
Developed during the **TOBB ETÜ Odoo Workshop**, following Odoo's official *Server Framework 101* tutorial.

<img width="1917" height="423" alt="image" src="https://github.com/user-attachments/assets/e7de8b1a-4e86-45d6-8f6b-becdae5d2fea" />

<img width="1917" height="732" alt="image" src="https://github.com/user-attachments/assets/903f5724-8029-489d-8442-68d8c9bd81c8" />


---

## Features

| Area | Description |
|------|-------------|
| **Property listings** | Price, living area, bedrooms, garden details; total area is computed automatically |
| **Offers** | Buyers submit offers; accept / refuse actions with business-rule validation |
| **Sales workflow** | `New → Offer Received → Offer Accepted → Sold` (or `Cancelled`) via statusbar |
| **Best offer tracking** | Highest offer is computed live from all related offers |
| **Property types & tags** | Categorisation with colour-coded tags; each type lists its properties |
| **Data integrity** | SQL and Python constraints (see below) |
| **UI feedback** | Colour-coded list views by state and offer status |

### Business rules

- Expected price must be strictly positive
- Selling price and offer prices must be positive
- Selling price cannot be lower than **90%** of the expected price
- Property type and tag names must be unique
- Cancelled properties cannot be sold; sold properties cannot be cancelled
- A property can only have one accepted offer; accepted offers cannot be refused

---

## Data Model

```
estate.property ──┬── Many2one ──► estate.property.type
                  ├── Many2many ─► estate.property.tag
                  ├── One2many ──► estate.property.offer ── Many2one ──► res.partner
                  ├── Many2one ──► res.partner   (buyer)
                  └── Many2one ──► res.users     (salesperson)
```

## Module Structure

```
estate/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── estate_property.py          # Main model, computed fields, actions, constraints
│   ├── estate_property_offer.py    # Offers with accept / refuse logic
│   ├── estate_property_type.py
│   └── estate_property_tag.py
├── views/
│   ├── estate_property_views.xml   # List + form views, statusbar, notebook
│   ├── estate_property_offer_views.xml
│   ├── estate_property_type_views.xml
│   ├── estate_property_tag_views.xml
│   └── estate_menus.xml
└── security/
    └── ir.model.access.csv         # Access rights for internal users
```

---

## Installation

1. Clone the repository into your Odoo addons path:
   ```bash
   git clone https://github.com/Sevvalgungorr/odoo19-real-estate.git estate
   ```
2. Make sure the folder is listed in `addons_path` in your `odoo.conf`.
3. Restart the Odoo server and update the module list:
   ```bash
   ./odoo-bin -c odoo.conf -d <database> -u estate
   ```
4. Go to **Apps**, search for **Real Estate** and install it.

## Usage

1. Open **Real Estate → Property Settings** and create a property.
2. Add offers from the **Offers** tab.
3. Accept an offer — buyer and selling price are filled in automatically.
4. Mark the property as **Sold** or **Cancel** it from the header buttons.

---

## Roadmap

- [ ] Search view with filters and group-by
- [ ] Offer validity / deadline (computed + inverse fields)
- [ ] Automatic `Offer Received` state on offer creation
- [ ] Deletion protection for active properties
- [ ] Salesperson's properties on the user form (`res.users` inheritance)
- [ ] Kanban view
- [ ] `estate_account` — automatic invoicing on sale

---

## Author

**Şevval Güngör** — Computer Engineering, Kırıkkale University
