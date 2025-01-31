## 1-qadam
Baza yaratish
```sql
CREATE DATABASE db_name
```
## 2-qadam
Jadval yaratish

```sql
CREATE TABLE harajatlar (
   id int NOT NULL AUTO_INCREMENT,
   sana date DEFAULT NULL,
   summa decimal(10,2) DEFAULT NULL,
   nom varchar(255) DEFAULT NULL,
   chat_id bigint DEFAULT NULL,
   PRIMARY KEY (id)
 ) 
```
```sql
CREATE TABLE savdolar (
   id int NOT NULL AUTO_INCREMENT,
   sana date DEFAULT NULL,
   summa decimal(10,2) DEFAULT NULL,
   chat_id bigint DEFAULT NULL,
   PRIMARY KEY (id)
 ) 
```

## 3-qadam
.env fayl yaratish

```
BOT_TOKEN=7999248628:AAGSmSARGSCMfpC6dVUx7j8PKSNkJnosub8
DB_HOST="localhost"
DB_USER="root"
DB_PASSWORD="root"
DB_NAME="oila3"
```