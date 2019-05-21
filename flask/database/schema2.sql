DROP TABLE IF EXISTS user;

CREATE TABLE ip_addresses (
  address TEXT UNIQUE NOT NULL,
);
CREATE TABLE mac_addresses (
   mac TEXT UNIQUE NOT NULL,
);
CREATE TABLE correlations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usetime DATETIME,
    address TEXT UNIQUE NOT NULL,
    mac TEXT UNIQUE NOT NULL,
    FOREIGN KEY(address) REFERENCES ip_addresses(address),
    FOREIGN KEY(mac) REFERENCES mac_addresses(mac)
);
