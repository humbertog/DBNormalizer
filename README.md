DBNormalizer
============

DB normalizer project DMKM

Following features:
- Import of database schemes (metadata) from a database instance; if no database connection is available, relational schemes may be prompted manually
- Specification and editing of functional dependencies (FDs)
- Testing if a given set of FDs is satisfied in a database table (only if a database connection is available)
- Computation of a minimal cover
- Determination of the attribute closure for a given attribute set
- Calculation of all candidate keys
- Normal Form (NF) testing from 1NF up to BCNF; FDs which violate a certain NF are reported to the user
Generation of a normalization proposal: synthesis of relations in 3NF is guaranteed; BCNF synthesis may be possible. Normalization includes computation of:
  - the new relations
  - functional dependencies for the new relations
  - all candidate keys for the new relations
  - normal forms of the new relations (3NF or BCNF)
  - If a database connection is established, a SQL script for database transformation is created. This script includes
  - DDL statements to create the new tables
  - Import and export of FDs and database schemes as XML files (not implememted in the GUI)
  - Import of FDs, automatically retrieved from a database
