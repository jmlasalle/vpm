# vpm
Virtual Property Manager (VPM) is the the true smarthome OS.

## Problem Statement
1. Homeowners are not professional property managers. They don't know what needs to be done to proactively maintain their home so that everything works, they minimize maintenance costs, and keep it in good condition.
2. Home maintenance information online is generic and often caveated. Most homeowners don't have the expertise to be confident they are appropriately interpreting and applying the general advice.
3. Homeowners have to develop their own information management and task management systems for their homes.
4. Tasks that would be quick for a professional property manager with experience and relationships, such as identifying what trade is needed to fix a problem, getting and assessing bids (including benchmarking to general market costs), and hiring a contractor they trust are much harder for homeowners who only need contractor service intermittently.
5. Smart home technology adds a layer of complexity and fragility to a home, rather than making homes more robust and self maintaining.

## Design Principles:
1. **Data Sovereignty:** You control your home's data in perpetuity.
2. **Portability:** conform to open standards with easy inport and export.
3. **Interoperability:** Do core functikns well, and integrate with other services 
4. **Unenshitifiable:** Product design must make it impossible to enshitify.

A smart home:
1. knows itself.
2. maintains itself
3. just works  

## products
### vpm-cli
CLI application to manage your home digital twin.
### vpm-api
Cloud based api to manage your home's digital twin and maintenance tasks.
### vpm-web
Web front end to interact with vpm-api.


## Product Structure
 1. Home digital twin
    1. Rooms
    2. Equipment
    3. Manuals 
 2. Maintance management --> automation
    1. Tasks
    2. Records
    3. Parts
    4. Automatic purchasing
 3. Chatbot: Tailored answers for your specific home.
 5. Contractor sourcing and management
    1. Bidding and contractor screening
    2. Specs generation
    3. Payments and record keeping

## Solution
### Core Offer
A smart home operating system that provides:
1. Information management for the home, including installed equipment (manuals, warranties, maintenance log), insurance and other documents,
2. Task management with maintenance tasks generated from the home information model


### Longterm roadmap
1. Automated purchasing and delivery for equipment that must be replaced on a schedule (e.g. air and water filters) or replacement parts that won't change (lightbulbs)
1. Chatbot trained on home info and manuals
2. Contractor hiring and pricing

## Technical Plan
### Core features
1. Database of installed equipment and home attributes based on the [IFC standard](https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/).
1. Maintenance tasks for installed equipment
1. Purchasing tasks linked to maintenance tasks and equipment
1. Log of maintenance activities, costs, etc.
1. Document database. Potentially [paperless-ngx](https://github.com/paperless-ngx/paperless-ngx).

### Tech Stack
* Backend: Python FastAPI - Modern, fast, easy to learn, good documentation.
* Frontend: React - Popular, large community, versatile for UI development.
* Database: SQLite - Robust, open-source, good all-around relational database.
* Communication: RESTful API (JSON over HTTP) - Simple and standard.

