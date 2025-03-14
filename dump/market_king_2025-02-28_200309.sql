-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: market_king
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add application',6,'add_application'),(22,'Can change application',6,'change_application'),(23,'Can delete application',6,'delete_application'),(24,'Can view application',6,'view_application'),(25,'Can add access token',7,'add_accesstoken'),(26,'Can change access token',7,'change_accesstoken'),(27,'Can delete access token',7,'delete_accesstoken'),(28,'Can view access token',7,'view_accesstoken'),(29,'Can add grant',8,'add_grant'),(30,'Can change grant',8,'change_grant'),(31,'Can delete grant',8,'delete_grant'),(32,'Can view grant',8,'view_grant'),(33,'Can add refresh token',9,'add_refreshtoken'),(34,'Can change refresh token',9,'change_refreshtoken'),(35,'Can delete refresh token',9,'delete_refreshtoken'),(36,'Can view refresh token',9,'view_refreshtoken'),(37,'Can add id token',10,'add_idtoken'),(38,'Can change id token',10,'change_idtoken'),(39,'Can delete id token',10,'delete_idtoken'),(40,'Can view id token',10,'view_idtoken'),(41,'Can add association',11,'add_association'),(42,'Can change association',11,'change_association'),(43,'Can delete association',11,'delete_association'),(44,'Can view association',11,'view_association'),(45,'Can add code',12,'add_code'),(46,'Can change code',12,'change_code'),(47,'Can delete code',12,'delete_code'),(48,'Can view code',12,'view_code'),(49,'Can add nonce',13,'add_nonce'),(50,'Can change nonce',13,'change_nonce'),(51,'Can delete nonce',13,'delete_nonce'),(52,'Can view nonce',13,'view_nonce'),(53,'Can add user social auth',14,'add_usersocialauth'),(54,'Can change user social auth',14,'change_usersocialauth'),(55,'Can delete user social auth',14,'delete_usersocialauth'),(56,'Can view user social auth',14,'view_usersocialauth'),(57,'Can add partial',15,'add_partial'),(58,'Can change partial',15,'change_partial'),(59,'Can delete partial',15,'delete_partial'),(60,'Can view partial',15,'view_partial'),(61,'Can add multi factor auth',16,'add_multifactorauth'),(62,'Can change multi factor auth',16,'change_multifactorauth'),(63,'Can delete multi factor auth',16,'delete_multifactorauth'),(64,'Can view multi factor auth',16,'view_multifactorauth'),(65,'Can add ユーザー',17,'add_user'),(66,'Can change ユーザー',17,'change_user'),(67,'Can delete ユーザー',17,'delete_user'),(68,'Can view ユーザー',17,'view_user'),(69,'Can add Token',18,'add_token'),(70,'Can change Token',18,'change_token'),(71,'Can delete Token',18,'delete_token'),(72,'Can view Token',18,'view_token'),(73,'Can add token',19,'add_tokenproxy'),(74,'Can change token',19,'change_tokenproxy'),(75,'Can delete token',19,'delete_tokenproxy'),(76,'Can view token',19,'view_tokenproxy'),(77,'Can add service',20,'add_service'),(78,'Can change service',20,'change_service'),(79,'Can delete service',20,'delete_service'),(80,'Can view service',20,'view_service'),(81,'Can add shipping',21,'add_shipping'),(82,'Can change shipping',21,'change_shipping'),(83,'Can delete shipping',21,'delete_shipping'),(84,'Can view shipping',21,'view_shipping'),(85,'Can add countries',22,'add_countries'),(86,'Can change countries',22,'change_countries'),(87,'Can delete countries',22,'delete_countries'),(88,'Can view countries',22,'view_countries'),(89,'Can add shipping surcharge',23,'add_shippingsurcharge'),(90,'Can change shipping surcharge',23,'change_shippingsurcharge'),(91,'Can delete shipping surcharge',23,'delete_shippingsurcharge'),(92,'Can view shipping surcharge',23,'view_shippingsurcharge'),(93,'Can add setting',24,'add_setting'),(94,'Can change setting',24,'change_setting'),(95,'Can delete setting',24,'delete_setting'),(96,'Can view setting',24,'view_setting'),(97,'Can add user',25,'add_user'),(98,'Can change user',25,'change_user'),(99,'Can delete user',25,'delete_user'),(100,'Can view user',25,'view_user'),(101,'Can add blacklisted token',26,'add_blacklistedtoken'),(102,'Can change blacklisted token',26,'change_blacklistedtoken'),(103,'Can delete blacklisted token',26,'delete_blacklistedtoken'),(104,'Can view blacklisted token',26,'view_blacklistedtoken'),(105,'Can add outstanding token',27,'add_outstandingtoken'),(106,'Can change outstanding token',27,'change_outstandingtoken'),(107,'Can delete outstanding token',27,'delete_outstandingtoken'),(108,'Can view outstanding token',27,'view_outstandingtoken'),(109,'Can add ebay token',28,'add_ebaytoken'),(110,'Can change ebay token',28,'change_ebaytoken'),(111,'Can delete ebay token',28,'delete_ebaytoken'),(112,'Can view ebay token',28,'view_ebaytoken'),(113,'Can add ebay store type',29,'add_ebaystoretype'),(114,'Can change ebay store type',29,'change_ebaystoretype'),(115,'Can delete ebay store type',29,'delete_ebaystoretype'),(116,'Can view ebay store type',29,'view_ebaystoretype'),(117,'Can add tax',30,'add_tax'),(118,'Can change tax',30,'change_tax'),(119,'Can delete tax',30,'delete_tax'),(120,'Can view tax',30,'view_tax'),(121,'Can add status',31,'add_status'),(122,'Can change status',31,'change_status'),(123,'Can delete status',31,'delete_status'),(124,'Can view status',31,'view_status'),(125,'Can add ebay register from yahoo auction',32,'add_ebayregisterfromyahooauction'),(126,'Can change ebay register from yahoo auction',32,'change_ebayregisterfromyahooauction'),(127,'Can delete ebay register from yahoo auction',32,'delete_ebayregisterfromyahooauction'),(128,'Can view ebay register from yahoo auction',32,'view_ebayregisterfromyahooauction'),(129,'Can add condition',33,'add_condition'),(130,'Can change condition',33,'change_condition'),(131,'Can delete condition',33,'delete_condition'),(132,'Can view condition',33,'view_condition'),(133,'Can add yahoo auction status',34,'add_yahooauctionstatus'),(134,'Can change yahoo auction status',34,'change_yahooauctionstatus'),(135,'Can delete yahoo auction status',34,'delete_yahooauctionstatus'),(136,'Can view yahoo auction status',34,'view_yahooauctionstatus'),(137,'Can add yahoo auction',35,'add_yahooauction'),(138,'Can change yahoo auction',35,'change_yahooauction'),(139,'Can delete yahoo auction',35,'delete_yahooauction'),(140,'Can view yahoo auction',35,'view_yahooauction'),(141,'Can add yahoo free market',36,'add_yahoofreemarket'),(142,'Can change yahoo free market',36,'change_yahoofreemarket'),(143,'Can delete yahoo free market',36,'delete_yahoofreemarket'),(144,'Can view yahoo free market',36,'view_yahoofreemarket'),(145,'Can add ebay',37,'add_ebay'),(146,'Can change ebay',37,'change_ebay'),(147,'Can delete ebay',37,'delete_ebay'),(148,'Can view ebay',37,'view_ebay'),(149,'Can add yahoo free market status',38,'add_yahoofreemarketstatus'),(150,'Can change yahoo free market status',38,'change_yahoofreemarketstatus'),(151,'Can delete yahoo free market status',38,'delete_yahoofreemarketstatus'),(152,'Can view yahoo free market status',38,'view_yahoofreemarketstatus');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(33,'api','condition'),(22,'api','countries'),(37,'api','ebay'),(32,'api','ebayregisterfromyahooauction'),(29,'api','ebaystoretype'),(28,'api','ebaytoken'),(20,'api','service'),(24,'api','setting'),(21,'api','shipping'),(23,'api','shippingsurcharge'),(31,'api','status'),(30,'api','tax'),(17,'api','user'),(35,'api','yahooauction'),(34,'api','yahooauctionstatus'),(36,'api','yahoofreemarket'),(38,'api','yahoofreemarketstatus'),(3,'auth','group'),(2,'auth','permission'),(25,'auth','user'),(18,'authtoken','token'),(19,'authtoken','tokenproxy'),(4,'contenttypes','contenttype'),(16,'drf_social_oauth2','multifactorauth'),(7,'oauth2_provider','accesstoken'),(6,'oauth2_provider','application'),(8,'oauth2_provider','grant'),(10,'oauth2_provider','idtoken'),(9,'oauth2_provider','refreshtoken'),(5,'sessions','session'),(11,'social_django','association'),(12,'social_django','code'),(13,'social_django','nonce'),(15,'social_django','partial'),(14,'social_django','usersocialauth'),(26,'token_blacklist','blacklistedtoken'),(27,'token_blacklist','outstandingtoken');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-01-28 22:37:34.659285'),(2,'contenttypes','0002_remove_content_type_name','2025-01-28 22:37:34.752286'),(3,'auth','0001_initial','2025-01-28 22:37:35.113775'),(4,'auth','0002_alter_permission_name_max_length','2025-01-28 22:37:35.218478'),(5,'auth','0003_alter_user_email_max_length','2025-01-28 22:37:35.230479'),(6,'auth','0004_alter_user_username_opts','2025-01-28 22:37:35.241478'),(7,'auth','0005_alter_user_last_login_null','2025-01-28 22:37:35.253476'),(8,'auth','0006_require_contenttypes_0002','2025-01-28 22:37:35.260478'),(9,'auth','0007_alter_validators_add_error_messages','2025-01-28 22:37:35.269478'),(10,'auth','0008_alter_user_username_max_length','2025-01-28 22:37:35.280479'),(11,'auth','0009_alter_user_last_name_max_length','2025-01-28 22:37:35.296478'),(12,'auth','0010_alter_group_name_max_length','2025-01-28 22:37:35.323478'),(13,'auth','0011_update_proxy_permissions','2025-01-28 22:37:35.337479'),(14,'auth','0012_alter_user_first_name_max_length','2025-01-28 22:37:35.350758'),(15,'api','0001_initial','2025-01-28 22:37:35.803759'),(16,'admin','0001_initial','2025-01-28 22:37:35.999095'),(17,'admin','0002_logentry_remove_auto_add','2025-01-28 22:37:36.009095'),(18,'admin','0003_logentry_add_action_flag_choices','2025-01-28 22:37:36.018455'),(19,'oauth2_provider','0001_initial','2025-01-28 22:37:37.031990'),(20,'oauth2_provider','0002_auto_20190406_1805','2025-01-28 22:37:37.118699'),(21,'oauth2_provider','0003_auto_20201211_1314','2025-01-28 22:37:37.218094'),(22,'oauth2_provider','0004_auto_20200902_2022','2025-01-28 22:37:37.758773'),(23,'oauth2_provider','0005_auto_20211222_2352','2025-01-28 22:37:37.804791'),(24,'oauth2_provider','0006_alter_application_client_secret','2025-01-28 22:37:37.833784'),(25,'oauth2_provider','0007_application_post_logout_redirect_uris','2025-01-28 22:37:37.941658'),(26,'oauth2_provider','0008_alter_accesstoken_token','2025-01-28 22:37:37.955658'),(27,'oauth2_provider','0009_add_hash_client_secret','2025-01-28 22:37:38.027677'),(28,'oauth2_provider','0010_application_allowed_origins','2025-01-28 22:37:38.162162'),(29,'oauth2_provider','0011_refreshtoken_token_family','2025-01-28 22:37:38.203160'),(30,'oauth2_provider','0012_add_token_checksum','2025-01-28 22:37:38.518372'),(31,'sessions','0001_initial','2025-01-28 22:37:38.573372'),(32,'default','0001_initial','2025-01-28 22:37:38.917221'),(33,'social_auth','0001_initial','2025-01-28 22:37:38.924221'),(34,'default','0002_add_related_name','2025-01-28 22:37:38.945219'),(35,'social_auth','0002_add_related_name','2025-01-28 22:37:38.953221'),(36,'default','0003_alter_email_max_length','2025-01-28 22:37:38.977223'),(37,'social_auth','0003_alter_email_max_length','2025-01-28 22:37:38.983221'),(38,'default','0004_auto_20160423_0400','2025-01-28 22:37:39.004336'),(39,'social_auth','0004_auto_20160423_0400','2025-01-28 22:37:39.012219'),(40,'social_auth','0005_auto_20160727_2333','2025-01-28 22:37:39.051238'),(41,'social_django','0006_partial','2025-01-28 22:37:39.128220'),(42,'social_django','0007_code_timestamp','2025-01-28 22:37:39.209305'),(43,'social_django','0008_partial_timestamp','2025-01-28 22:37:39.283305'),(44,'social_django','0009_auto_20191118_0520','2025-01-28 22:37:39.402285'),(45,'social_django','0010_uid_db_index','2025-01-28 22:37:39.472477'),(46,'social_django','0011_alter_id_fields','2025-01-28 22:37:40.091954'),(47,'social_django','0012_usersocialauth_extra_data_new','2025-01-28 22:37:40.361612'),(48,'social_django','0013_migrate_extra_data','2025-01-28 22:37:40.395777'),(49,'social_django','0014_remove_usersocialauth_extra_data','2025-01-28 22:37:40.494777'),(50,'social_django','0015_rename_extra_data_new_usersocialauth_extra_data','2025-01-28 22:37:40.581777'),(51,'social_django','0016_alter_usersocialauth_extra_data','2025-01-28 22:37:40.603777'),(52,'social_django','0002_add_related_name','2025-01-28 22:37:40.617775'),(53,'social_django','0004_auto_20160423_0400','2025-01-28 22:37:40.623779'),(54,'social_django','0003_alter_email_max_length','2025-01-28 22:37:40.634780'),(55,'social_django','0005_auto_20160727_2333','2025-01-28 22:37:40.643777'),(56,'social_django','0001_initial','2025-01-28 22:37:40.651868'),(57,'api','0002_user_family_name_user_given_name_user_name_and_more','2025-01-29 06:47:24.671889'),(61,'api','0003_service_countries_shipping','2025-01-29 17:56:35.874728'),(62,'api','0004_alter_service_service_name','2025-01-29 18:13:36.102144'),(66,'api','0005_shippingsurcharge','2025-01-30 18:25:37.605919'),(67,'api','0006_migrate_settings_data','2025-01-30 18:25:37.784557'),(68,'api','0007_remove_user_yahoo_client_id_and_more','2025-01-30 18:25:37.947066'),(69,'authtoken','0001_initial','2025-01-30 18:25:38.183166'),(70,'authtoken','0002_auto_20160226_1747','2025-01-30 18:25:38.221785'),(71,'authtoken','0003_tokenproxy','2025-01-30 18:25:38.231301'),(72,'api','0008_setting_ebay_dev_id','2025-01-31 17:25:37.701746'),(73,'api','0009_setting_ebay_user_token','2025-01-31 18:54:47.217269'),(74,'api','0010_rename_ebay_user_token_setting_ebay_refresh_token','2025-01-31 19:04:50.043820'),(75,'api','0011_rename_ebay_refresh_token_setting_ebay_auth_token','2025-01-31 19:08:05.781683'),(76,'api','0012_remove_setting_ebay_auth_token_and_more','2025-02-03 02:33:03.688250'),(77,'api','0013_user_profile_picture_alter_setting_id_and_more','2025-02-03 03:18:09.828981'),(78,'api','0013_alter_setting_id','2025-02-03 13:59:56.037939'),(79,'api','0014_setting_ebay_access_token_and_more','2025-02-03 17:51:28.754262'),(80,'api','0015_setting_rate','2025-02-08 07:28:59.729084'),(81,'api','0016_setting_deepl_api_key','2025-02-08 08:30:25.879056'),(82,'token_blacklist','0001_initial','2025-02-10 04:29:58.732271'),(83,'token_blacklist','0002_outstandingtoken_jti_hex','2025-02-10 04:29:58.775301'),(84,'token_blacklist','0003_auto_20171017_2007','2025-02-10 04:29:58.794304'),(85,'token_blacklist','0004_auto_20171017_2013','2025-02-10 04:29:58.902412'),(86,'token_blacklist','0005_remove_outstandingtoken_jti','2025-02-10 04:29:58.983951'),(87,'token_blacklist','0006_auto_20171017_2113','2025-02-10 04:29:59.028203'),(88,'token_blacklist','0007_auto_20171017_2214','2025-02-10 04:29:59.342504'),(89,'token_blacklist','0008_migrate_to_bigautofield','2025-02-10 04:29:59.666892'),(90,'token_blacklist','0010_fix_migrate_to_bigautofield','2025-02-10 04:29:59.679893'),(91,'token_blacklist','0011_linearizes_history','2025-02-10 04:29:59.684935'),(92,'token_blacklist','0012_alter_outstandingtoken_user','2025-02-10 04:29:59.694608'),(93,'api','0017_remove_setting_ebay_access_token_and_more','2025-02-11 13:54:16.058702'),(94,'api','0018_setting_user','2025-02-11 17:41:54.484751'),(95,'api','0019_ebaystoretype','2025-02-16 16:45:44.503219'),(96,'api','0020_alter_ebaystoretype_final_value_fee_and_more','2025-02-16 16:50:52.037230'),(97,'api','0021_setting_ebay_store_type','2025-02-16 16:52:48.809431'),(98,'api','0022_ebaystoretype_international_fee','2025-02-16 17:13:15.929873'),(99,'api','0023_alter_ebaystoretype_international_fee','2025-02-16 17:13:42.292908'),(100,'api','0024_tax','2025-02-16 17:15:24.930491'),(101,'api','0025_status','2025-02-18 13:47:26.037607'),(102,'api','0026_alter_countries_service_and_more','2025-02-18 13:50:34.868444'),(103,'api','0027_ebayregisterfromyahooauction_user_and_more','2025-02-18 17:34:08.410497'),(104,'api','0028_condition','2025-02-19 17:25:13.400547'),(105,'api','0029_ebayregisterfromyahooauction_offer_id','2025-02-20 15:23:14.243629'),(106,'api','0030_alter_ebayregisterfromyahooauction_offer_id','2025-02-20 15:32:11.967756'),(107,'api','0031_setting_description_template_1_and_more','2025-02-24 12:11:48.133349'),(108,'api','0032_setting_description_template_3','2025-02-24 12:58:28.846642'),(109,'api','0031_yahooauctionstatus_setting_description_template_1_and_more','2025-02-24 15:25:03.557617'),(110,'api','0032_ebayregisterfromyahooauction_yahoo_auction_status_and_more','2025-02-24 15:26:57.690971'),(111,'api','0002_yahooauction_yahoofreemarket_ebay_and_more','2025-02-25 14:12:14.938673'),(112,'api','0003_rename_ebay_sku_c3b181_idx_t_ebay_sku_a442ba_idx_and_more','2025-02-25 14:13:57.733699'),(113,'api','0004_remove_yahoofreemarket_end_time','2025-02-26 15:26:25.103415'),(114,'api','0005_yahoofreemarketstatus_alter_yahoofreemarket_status','2025-02-26 15:29:33.075144');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4wexi0no0hp1y8he25rqex6bo5cz4w9v','.eJxVjMsOwiAQRf-FtSEdyqO4dO83EIYZpGogKe3K-O_apAvd3nPOfYkQt7WErfMSZhJnAeL0u2FMD647oHustyZTq-syo9wVedAur434eTncv4MSe_nWAzPmqHUy1qB3ymkHztiMCjxONLKynpI1o_bgNQEb8IzK4WQykB3E-wPYoTdY:1tcuEd:wiiJPaL3kbAOzNawVhXxWvOVsMXb72-USbNiDsghfIs','2025-02-11 22:39:07.352764');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;

--
-- Table structure for table `ebay_tokens`
--

DROP TABLE IF EXISTS `ebay_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ebay_tokens` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `access_token` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `refresh_token` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `scope` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ebay_tokens_user_id_daaae8bb_fk_users_id` (`user_id`),
  CONSTRAINT `ebay_tokens_user_id_daaae8bb_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ebay_tokens`
--

/*!40000 ALTER TABLE `ebay_tokens` DISABLE KEYS */;
INSERT INTO `ebay_tokens` VALUES (17,'gAAAAABnwYRoiU8CLf0l3qc0iNZS0Rhj0PTKEQHw4ZlFARiA-P3prU0_hF4WJH_BvFBSlnbX9I7kbinaNKAAVEJAuBowuQ72AXaSnbNFswBvGIyofKNOGfKoM-IE40lgic2sscPbtLTtSRydlGMz9VUISICD7rd_3YK1U3rEMSS8mvU-ljpzkRSYqvxleIMc8t7REj3pGlcqlEqR7hTpPuoa1SEHjhL7CPSnz0Rdk8S9NQb_TsmZR2KXbkDb-v5_R3bHzPTtGPhaCnL3YcuRDjRPa5zg2r44NIF4VG8bdj-PTVLATdruF6WqdCMxADYEWzDcRr-dd3duS4pB3UYv0Sef25_6WNUgnQPlyI3HyXGMC9XfIXh5otpj1AK2F2SHJ7t7PhgGssaQo8B8prcaTOMxjJGsTcOByvVGmudIUvVpS_oVZTxEnUeMMblRnsfXO6StXhUYpf90eyE9fuNMFz-iy8R7NoFCCO0hu7Nky_ucqRq__JmwRjzkOntTBPLtjF0DmuT3ewBP82iQK0Fg65jFRjWHdF9p3-fCLcfCtLvFFp9oGjZ_hXTI24IUp9b7R9oIUR42j-44RG-_J0FGfmNkQmnBlkNTdPGK9wOU8pEAS2XjNjBrx22vBVbRj_O6hvpcFvPHzyjdJViB1nRHIVqQV2evlMTl6qF2od7hleIMYDLcRED4xXE415icNWZpQjy6iIHZhEYurtnte-eobq6t3shYTGHNwhWnhkrw2Nd8lTRRH51JPW8A8cUtovT8xwXBnH9LpcA7f_IZe2HRU1ENzn0JlJkA2O883uub2rzuPYFSY3Hq3k5q3joaSYGA0P3PFt6-3DGI-LJuOfPMnM3unabqhZ-Dnm23UcacW2AUOpvi8DMv08SHZg8Epq8VjK6sfjlZ7zPTVth0idPb_Fu_4TZl-ic2VfzTGa4W-PneHgrK-AV99NYiJrtxQ-kKYDD9hrX9GD8LNdNFrevXp-LXRwSnQWfYr7lH2MZdtUBcYh84JUDjmO_IFLVec4S4iMKeWuybvTSrn3nJKpXj7duAyaheJjyOa6iK5DV--1PNM-w3SGpa-4NQVtxEKJpkpR7yFImCsUENu42GTL3nIkYFF6SVosN4Stg0JrOoUinAVgRg87iPzyPt76d9PGls4Uog22P9aOmLiW8L9ygFCggpZgF2JYDIFvacO1PWzPU-awtKFVFMs9cxVC_GLNjQOmV9K6UXdI-OIF8siCMHB9rk4JDb5q6BRy_VOWEZSNIHJU0HqMqHKAbWO3BN5VqLg6WblQaZYkJJFeOxXwB1XfBlFK3RIf-7uuunM36mE7jyPk9j36JVkfCxGlqG6brlAg0S9gYs6AQMK6X5AF1jwZc_EjYZqpepCszKyHFugSu9WyLblEuk8W-NKMnXWDyWHJy0NIeok1OfRtwB5qgPXxp-RMPajkoskXYgOkePZwt6eCpsNvaTFlR3zAvcWmpfyHflSI-Al6eJla9LcGtmMRbBgqLYt7MjmTT-FW_dYBx5RNK9_5YV4IcxoYBMqNcDbgWU3P-bjuJn3GQrb7hF3lggLR6nLf0itZLrPDg-QHWimChE1894Uvvgf6RBzxMwRe1uxvrIUocOm6lGpQ6uIzUEbtYanGPvsRRrkBeVccVKr3tRU8iehh5ZoW6_pa3Lx4WCFLZHnjr0vomnBsLP45Y6sZkIJtbUYaf93ZJgEwSgSPYYP0pIHccOnjZiYBPpIr4wWOQKz_Vzj3zvSQjNBJiWhPdEMRd-Eks3MWF-YtRcQRXgOjokBtwj1y71BtA6mMyrDrLbXBoo8JzODU4bCgONhgpIy2eE0Npz-lPbhpSHn3nOkVNOVquTD6txHPCObKYuXKKVt6tabBP6vCjIAZ4_yPLXKKUbqYejG1FruFTZMzj-P5beZo3uDPo-uGVN_UItn2VmEd10LOGH6Y0swFv0Mzf-SoUgxCf_yKJLWx0CR2lcdvvCPxHMBoR2VVV67fKIErvgVX_kGKA7EBUsVSalNZld0jXR7-sKvSfCYrKBpRhoHrrOrc3fJXvIzBhb0tN0h-tZsfRmVV_oXM-IHAVC4SlSOwLct-zLPvQSC1auRaeK9G8KmRmID7pKNBCWDdovEnzn5fnjRXSv8kMg2KncVCItBOgprpX0lot2tSbqG5l-KUgILBtrDAP5nJ_NUi7xXzJYJJ07R-EazVfTpfL-9dR-K0GvjsZepU-yfhkYLNm1FBp9XtoBBQ3g2wa3A1fxnvqs-GzqIYvER0e0ovbis9QR1EFKVlPab6yqpmzh34xCUJpJQ22rZ1NiLVOUHqm0gxJhfIzupLSmiiI0zy0I3MiymZCDxyrD_7TyIqc75OwWtEK6-dMMCvNeFWJ71CVB6D4R-ON6ofELkGVIyfzX3Ibzq--IJk0rLwOMPLdx3mUUUjWdPdO2sxKhnPR6MqsvHLagvbD51Q-ZRlOFYl3C_iyzqVocJBHDUUPl_AmsDqxssTLlRbrAwWc6nnukScZc5LCDlcl2IaUrBYvz19FFrEhLTopr586iuiylQP3dnud-tHWOrmysQ16Fhf0W7STL4DKMhrDHeNWgRaGdp_2ZBsTnKck7Kg5pgIWlJRMvSKBwS0t61V87FGKE7ySYAHibd1CUio8oQSRCpd-NlkmKfV0lzHINbDG7fXnZkT-v-OK9wtFk5_wbZFqeX7F6E5eKhfVWKKntcH6ulqHLdAYwENTp9RJ4r-hIKP8AhzQ8DaNF7cQSUJL2NdQOBBvfas1K3Q0ztYibjqFDA15MAYa4GpPJQVtS52D1gnivJI-86XX-LMOakiWgdAQREe7KfB4Kz17dJezudMW9WQ-j2XcNH-nTjx0ObveRzUgkUkceSgPxjoTgcKB9u4i9xy-eV4VD8ztjE33vsh5IhkavR19d_DBFyuUMrN5M7ORnNS2Kc2IU_Grt6rRFZIRoi-9YyMAlsmj0x5pRbuWIA3o4B5u1Ni1enYjHr2_1FbQliWCg3b2VFSbQOtVqSGsfMz1LIVAm087hguNFeV1OPoVG0_O13RCsaXXljih9MSnHskQndfwbXiUXPOPf37blBCA33jUc-f1grWwcAHtfmUGMHamIVO9TaQlik_wNCCiLqasEi1RjXGSuMO5RHPbXO33eyiUuL0kJWs4E91tXKkVE9zB3tK3EPzqLQZJvKqZRtEmxGzcyNW6OtAIrak92ygQUHr4vMIhBziq-woApC2ipJVnsrkaf5gjy7xiCK6rY80g2QaaDxmnBBMQlMtzy5HOS0KK4T-EAKNY6OpD9cPYDuveg1sU4xk6lE3o19ohfzBmD4NW8p1_jt6uo9HKAMlRMHLpB448K2jGN','gAAAAABnwYRozJu7gL0ZDgokGEQdOlg3KfwgfYr4zBV-gn4KlcktxTYT5RrHGQ41pSwNDzz0jKduWGT-iu6nVLvL70vItUrDYFpNWmFt0z4OBamKiBjt8clTW9JSXza1bFCqryK-EiJxP9CBWZ7pKEdyddz_2MWKJvE8HrhuLqglt9zmvfk2k3XdonuVqrM7ZvE7PYZqdeknsn8TeBr8kVRq5OP50hZ0qg==','2025-02-28 11:39:52.573387','https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.marketing.readonly https://api.ebay.com/oauth/api_scope/sell.marketing https://api.ebay.com/oauth/api_scope/sell.inventory.readonly https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account.readonly https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly https://api.ebay.com/oauth/api_scope/sell.fulfillment https://api.ebay.com/oauth/api_scope/sell.analytics.readonly https://api.ebay.com/oauth/api_scope/sell.finances https://api.ebay.com/oauth/api_scope/sell.payment.dispute https://api.ebay.com/oauth/api_scope/commerce.identity.readonly','2025-02-27 07:19:45.884765','2025-02-28 09:39:52.574547',5);
/*!40000 ALTER TABLE `ebay_tokens` ENABLE KEYS */;

--
-- Table structure for table `m_condition`
--

DROP TABLE IF EXISTS `m_condition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_condition` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `condition_id` int NOT NULL,
  `condition_enum` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `m_condition`
--

/*!40000 ALTER TABLE `m_condition` DISABLE KEYS */;
INSERT INTO `m_condition` VALUES (1,1000,'NEW'),(2,1500,'NEW_OTHER'),(3,1750,'NEW_WITH_DEFECTS'),(4,2000,'CERTIFIED_REFURBISHED'),(5,2010,'EXCELLENT_REFURBISHED'),(6,2020,'VERY_GOOD_REFURBISHED'),(7,2030,'GOOD_REFURBISHED'),(8,2500,'SELLER_REFURBISHED'),(9,2750,'LIKE_NEW'),(10,2990,'PRE_OWNED_EXCELLENT'),(11,3000,'USED_EXCELLENT'),(12,3010,'PRE_OWNED_FAIR'),(13,4000,'USED_VERY_GOOD'),(14,5000,'USED_GOOD'),(15,6000,'USED_ACCEPTABLE'),(16,7000,'FOR_PARTS_OR_NOT_WORKING');
/*!40000 ALTER TABLE `m_condition` ENABLE KEYS */;

--
-- Table structure for table `m_countries`
--

DROP TABLE IF EXISTS `m_countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_countries` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `country_code` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `country_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `country_name_jp` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `zone` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `service_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `country_code` (`country_code`),
  KEY `m_countries_service_id_cdbbd3e6_fk_m_service_id` (`service_id`),
  CONSTRAINT `m_countries_service_id_cdbbd3e6_fk_m_service_id` FOREIGN KEY (`service_id`) REFERENCES `m_service` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `m_countries`
--

/*!40000 ALTER TABLE `m_countries` DISABLE KEYS */;
INSERT INTO `m_countries` VALUES (1,'AG','Antigua','アンティグア','A',1),(2,'TT','Trinidad and Tobago','トリニダード・トバゴ','A',1),(3,'AS','American Samoa','米領サモア','D',1),(4,'BN','Brunei','ブルネイ','D',1),(5,'KH','Cambodia','カンボジア','D',1),(6,'CK','Cook Islands','クック諸島','D',1),(7,'FJ','Fiji','フィジー','D',1),(8,'PF','French Polynesia','仏領ポリネシア','D',1),(9,'GU','Guam','グアム','D',1),(10,'LA','Laos','ラオス','D',1),(11,'MH','Marshall Islands','マーシャル諸島','D',1),(12,'FM','Micronesia','ミクロネシア','D',1),(13,'MN','Mongolia','モンゴル','D',1),(14,'MP','Northern Mariana Islands','北マリアナ諸島','D',1),(15,'NC','New Caledonia','ニューカレドニア','D',1),(16,'PW','Palau','パラオ','D',1),(17,'PG','Papua New Guinea','パプアニューギニア','D',1),(18,'WS','Samoa','サモア','D',1),(19,'TO','Tonga','トンガ','D',1),(20,'VU','Vanuatu','バヌアツ','D',1),(21,'WF','Wallis and Futuna','ウォリス・フツナ','D',1),(22,'AT','Austria','オーストリア','H',1),(23,'CZ','Czech Republic','チェコ','H',1),(24,'DK','Denmark','デンマーク','H',1),(25,'FI','Finland','フィンランド','H',1),(26,'GR','Greece','ギリシャ','H',1),(27,'GL','Greenland','グリーンランド','H',1),(28,'HU','Hungary','ハンガリー','H',1),(29,'IE','Ireland','アイルランド','H',1),(30,'IL','Israel','イスラエル','H',1),(31,'LI','Liechtenstein','リヒテンシュタイン','H',1),(32,'LU','Luxembourg','ルクセンブルグ','H',1),(33,'MC','Monaco','モナコ','H',1),(34,'NO','Norway','ノルウェー','H',1),(35,'PL','Poland','ポーランド','H',1),(36,'PT','Portugal','ポルトガル','H',1),(37,'SK','Slovakia','スロバキア','H',1),(38,'SE','Sweden','スウェーデン','H',1),(39,'CH','Switzerland','スイス','H',1),(40,'AL','Albania','アルバニア','I',1),(41,'AD','Andorra','アンドラ','I',1),(42,'AM','Armenia','アルメニア','I',1),(43,'AZ','Azerbaijan','アゼルバイジャン','I',1),(44,'BH','Bahrain','バーレーン','I',1),(45,'BY','Belarus','ベラルーシ','I',1),(46,'BA','Bosnia and Herzegovina','ボスニア·ヘルツェゴビナ','I',1),(47,'BG','Bulgaria','ブルガリア','I',1),(48,'HR','Croatia','クロアチア','I',1),(49,'CY','Cyprus','キプロス','I',1),(50,'EE','Estonia','エストニア','I',1),(51,'GE','Georgia','グルジア','I',1),(52,'GI','Gibraltar','ジブラルタル','I',1),(53,'KZ','Kazakhstan','カザフスタン','I',1),(54,'KW','Kuwait','クウェート','I',1),(55,'KG','Kyrgyzstan','キルギス','I',1),(56,'LV','Latvia','ラトビア','I',1),(57,'LT','Lithuania','リトアニア','I',1),(58,'MK','Macedonia','マケドニア','I',1),(59,'MT','Malta','マルタ','I',1),(60,'AF','Afghanistan','アフガニスタン','J',1),(61,'DZ','Algeria','アルジェリア','J',1),(62,'AO','Angola','アンゴラ','J',1),(63,'BD','Bangladesh','バングラデシュ','J',1),(64,'BJ','Benin','ベナン','J',1),(65,'BT','Bhutan','ブータン','J',1),(66,'BW','Botswana','ボツワナ','J',1),(67,'BF','Burkina Faso','ブルキナファソ','J',1),(68,'BI','Burundi','ブルンジ','J',1),(69,'CM','Cameroon','カメルーン','J',1),(70,'CV','Cape Verde','カーポベルデ','J',1),(71,'TD','Chad','チャド','J',1),(72,'CG','Congo','コンゴ共和国','J',1),(73,'CD','Democratic Republic of the Congo','コンゴ民主共和国','J',1),(74,'DJ','Djibouti','ジブチ','J',1),(75,'EG','Egypt','エジプト','J',1),(76,'ER','Eritrea','エリトリア','J',1),(77,'ET','Ethiopia','エチオピア','J',1),(78,'GA','Gabon','ガボン','J',1),(79,'GM','Gambia','ガンビア','J',1),(80,'GH','Ghana','ガーナ','J',1),(81,'GN','Guinea','ギニア','J',1),(82,'CI','Ivory Coast','コートジボワール','J',1),(83,'JO','Jordan','ヨルダン','J',1),(84,'KE','Kenya','ケニア','J',1),(85,'LB','Lebanon','レバノン','J',1),(86,'LS','Lesotho','レソト','J',1),(87,'LR','Liberia','リベリア','J',1),(88,'LY','Libya','リビア','J',1),(89,'MG','Madagascar','マダガスカル','J',1),(90,'MW','Malawi','マラウイ','J',1),(91,'CN','China (South)','中国(南部)','K',1),(92,'GB','United Kingdom','イギリス','M',1),(93,'DE','Germany','ドイツ','M',1),(94,'IT','Italy','イタリア','M',1),(95,'FR','France','フランス','M',1),(96,'ES','Spain','スペイン','M',1),(97,'BE','Belgium','ベルギー','M',1),(98,'NL','Netherlands','オランダ','M',1),(99,'VA','Vatican City','バチカン市国(教廷)','M',1),(100,'AU','Australia','オーストラリア','U',1),(101,'NZ','New Zealand','ニュージーランド','U',1);
/*!40000 ALTER TABLE `m_countries` ENABLE KEYS */;

--
-- Table structure for table `m_ebay_store_type`
--

DROP TABLE IF EXISTS `m_ebay_store_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_ebay_store_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `store_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `monthly_fee` decimal(10,2) DEFAULT NULL,
  `monthly_fee_annual` decimal(10,2) DEFAULT NULL,
  `free_listings` int NOT NULL,
  `listing_fee_over_limit` decimal(4,2) NOT NULL,
  `final_value_fee` decimal(4,1) NOT NULL,
  `final_value_fee_category_discount` tinyint(1) NOT NULL,
  `international_fee` decimal(4,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `store_type` (`store_type`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `m_ebay_store_type`
--

/*!40000 ALTER TABLE `m_ebay_store_type` DISABLE KEYS */;
INSERT INTO `m_ebay_store_type` VALUES (1,'free',0.00,0.00,250,0.40,15.0,0,1.35),(2,'basic',27.95,21.95,1000,0.25,11.5,1,1.35),(3,'premium',74.95,59.95,10000,0.10,11.5,1,1.35),(4,'anchor',349.95,299.95,25000,0.05,11.5,1,1.35),(5,'enterprise',NULL,2999.95,100000,0.10,11.5,1,1.35);
/*!40000 ALTER TABLE `m_ebay_store_type` ENABLE KEYS */;

--
-- Table structure for table `m_service`
--

DROP TABLE IF EXISTS `m_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_service` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `service_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `m_service`
--

/*!40000 ALTER TABLE `m_service` DISABLE KEYS */;
INSERT INTO `m_service` VALUES (1,'SpeedPAK Japan – Ship via FedEx'),(2,'SpeedPAK Japan – Ship via DHL'),(3,'SpeedPAK Economy Japan');
/*!40000 ALTER TABLE `m_service` ENABLE KEYS */;

--
-- Table structure for table `m_setting`
--

DROP TABLE IF EXISTS `m_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_setting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `yahoo_client_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `yahoo_client_secret` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ebay_client_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ebay_client_secret` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `ebay_dev_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rate` int DEFAULT NULL,
  `deepl_api_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `ebay_store_type_id` bigint NOT NULL,
  `description_template_1` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `description_template_2` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `description_template_3` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `m_setting_user_id_93a8a20f_fk_users_id` (`user_id`),
  KEY `m_setting_ebay_store_type_id_b74e1d70_fk_m_ebay_store_type_id` (`ebay_store_type_id`),
  CONSTRAINT `m_setting_ebay_store_type_id_b74e1d70_fk_m_ebay_store_type_id` FOREIGN KEY (`ebay_store_type_id`) REFERENCES `m_ebay_store_type` (`id`),
  CONSTRAINT `m_setting_user_id_93a8a20f_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `m_setting`
--

/*!40000 ALTER TABLE `m_setting` DISABLE KEYS */;
INSERT INTO `m_setting` VALUES (1,'dj00aiZpPVdneThLZTRQenNDVCZzPWNvbnN1bWVyc2VjcmV0Jng9ZjM-','vkCrBnR8lNI68O7Vl0UC0oyZjzteMyZQwf5FW8p4','-MarketKi-PRD-567026e79-f37766b1','PRD-67026e79ec82-79e8-4357-8960-d737','2025-01-30 18:57:27.381518','2025-02-27 06:20:13.379114','63020785-d0b7-4683-b9dc-feb53dff4341',5,'09466755-aeed-4385-b387-5d09b540bcad:fx',5,2,'<div class=\"template__main main4 change-color-4 change-text-color\" style=\"background: #fff; border: 1px solid #000; padding: 0 20px 30px 20px !important; box-sizing: border-box; word-break: break-all;\"><h1 style=\"font-family: Verdana, sans-serif; font-weight: bold; font-size: 22px; margin: 30px 0; text-align: center; color: #111; word-break: break-word;\"></h1><section class=\"product_dec\" style=\"margin: 0; padding: 0 0 20px 0; color: #111; text-align: left;\"><h2 style=\"font-family: FontAwesome; font-weight: 900; position: relative; background-color: #eee; color: #111; margin-bottom: 15px; padding: 10px 20px;\">Description</h2><div class=\"product__intro\" property=\"description\" style=\"line-height: 24px; font-size: 14px; padding: 0 0px 10px;\">','<p>I do not know much about the product.</p><p>Please look at the pictures and make your decision.</p>','</div></section><aside><div class=\"aside__item\"><h2 style=\"font-family: FontAwesome; font-weight: 900; position: relative; background-color: #eee; color: #111; margin-bottom: 15px; padding: 10px 20px;\">Shipping</h2><div class=\"product__intro\" property=\"description\" style=\"line-height: 24px; font-size: 14px; padding: 0 0px 10px;\"><ol><li style=\"font-family: Verdana, sans-serif; font-size: 14px; color: #111;\">We always send the item with a tracking number. So please place an order without any concern on delivery. You can always track the delivery status.</li><li style=\"font-family: Verdana, sans-serif; font-size: 14px; color: #111;\">Shipping is only available to the address registered in eBay. If you want us to send another address, please change your address on eBay and then place an order.</li><li style=\"font-family: Verdana, sans-serif; font-size: 14px; color: #111;\">Shipping is available from Monday to Friday. Weekends are not available because freight (shipping) companies are closed.</li><li style=\"font-family: Verdana, sans-serif; font-size: 14px; color: #111;\">We do not mark merchandise values below value or mark items as “gifts” – Japan, US and International government regulations prohibit such behavior.</li></ol></div></div><h2 style=\"font-family: FontAwesome; font-weight: 900; position: relative; background-color: #eee; color: #111; margin-bottom: 15px; padding: 10px 20px;\">About Importer\'s Obligation</h2><div class=\"product__intro\" property=\"description\" style=\"line-height: 24px; font-size: 14px; padding: 0 10px 10px;\"><p style=\"font-family: Verdana, sans-serif; font-size: 14px; color: #111;\">Import duties, taxes, and charges are not included in the item price or shipping cost.</p><p style=\"font-family: Verdana, sans-serif; font-size: 14px; color: #111;\">These charges are the buyer\'s responsibility. Please check with your country\'s customs office to determine what these additional costs will be prior to bidding or buying.</p><p style=\"font-family: Verdana, sans-serif; font-size: 14px; color: #111;\">Thank you for your understanding.</p></div></aside></div>');
/*!40000 ALTER TABLE `m_setting` ENABLE KEYS */;

--
-- Table structure for table `m_shipping`
--

DROP TABLE IF EXISTS `m_shipping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_shipping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `zone` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `weight` int NOT NULL,
  `basic_price` decimal(10,2) NOT NULL,
  `service_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `m_shipping_service_id_884e2eaa_fk_m_service_id` (`service_id`),
  CONSTRAINT `m_shipping_service_id_884e2eaa_fk_m_service_id` FOREIGN KEY (`service_id`) REFERENCES `m_service` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=287 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `m_shipping`
--

/*!40000 ALTER TABLE `m_shipping` DISABLE KEYS */;
INSERT INTO `m_shipping` VALUES (23,'A',1,2839.00,1),(24,'D',1,6129.00,1),(25,'E',1,1984.00,1),(26,'F',1,2016.00,1),(27,'G',1,2350.00,1),(28,'H',1,1980.00,1),(29,'I',1,1999.00,1),(30,'J',1,1909.00,1),(31,'K',1,2365.00,1),(32,'M',1,1916.00,1),(33,'U',1,2609.00,1),(34,'A',1,3827.00,1),(35,'D',1,6868.00,1),(36,'E',1,2439.00,1),(37,'F',1,2478.00,1),(38,'G',1,3794.00,1),(39,'H',1,2442.00,1),(40,'I',1,2466.00,1),(41,'J',1,3081.00,1),(42,'K',1,2456.00,1),(43,'M',1,2237.00,1),(44,'U',1,2873.00,1),(45,'A',2,4386.00,1),(46,'D',2,8049.00,1),(47,'E',2,2666.00,1),(48,'F',2,2707.00,1),(49,'G',2,4830.00,1),(50,'H',2,2906.00,1),(51,'I',2,2881.00,1),(52,'J',2,4072.00,1),(53,'K',2,2519.00,1),(54,'M',2,2603.00,1),(55,'U',2,2883.00,1),(56,'A',2,4754.00,1),(57,'D',2,8890.00,1),(58,'E',2,2918.00,1),(59,'F',2,2963.00,1),(60,'G',2,5561.00,1),(61,'H',2,3265.00,1),(62,'I',2,3315.00,1),(63,'J',2,4440.00,1),(64,'K',2,2730.00,1),(65,'M',2,2925.00,1),(66,'U',2,3185.00,1),(67,'A',3,5127.00,1),(68,'D',3,9731.00,1),(69,'E',3,3173.00,1),(70,'F',3,3224.00,1),(71,'G',3,6299.00,1),(72,'H',3,3627.00,1),(73,'I',3,3750.00,1),(74,'J',3,4810.00,1),(75,'K',3,2945.00,1),(76,'M',3,3249.00,1),(77,'U',3,3486.00,1),(78,'A',3,5493.00,1),(79,'D',3,10510.00,1),(80,'E',3,3329.00,1),(81,'F',3,3374.00,1),(82,'G',3,8604.00,1),(83,'H',3,3818.00,1),(84,'I',3,4023.00,1),(85,'J',3,6611.00,1),(86,'K',3,3156.00,1),(87,'M',3,3273.00,1),(88,'U',3,3766.00,1),(89,'A',4,5860.00,1),(90,'D',4,11290.00,1),(91,'E',4,3382.00,1),(92,'F',4,3424.00,1),(93,'G',4,9555.00,1),(94,'H',4,3907.00,1),(95,'I',4,4148.00,1),(96,'J',4,7472.00,1),(97,'K',4,3366.00,1),(98,'M',4,3327.00,1),(99,'U',4,4045.00,1),(100,'A',4,6227.00,1),(101,'D',4,12069.00,1),(102,'E',4,3786.00,1),(103,'F',4,3833.00,1),(104,'G',4,10442.00,1),(105,'H',4,4248.00,1),(106,'I',4,4554.00,1),(107,'J',4,8226.00,1),(108,'K',4,3577.00,1),(109,'M',4,3615.00,1),(110,'U',4,4323.00,1),(111,'A',5,6594.00,1),(112,'D',5,12848.00,1),(113,'E',5,4188.00,1),(114,'F',5,4242.00,1),(115,'G',5,11329.00,1),(116,'H',5,4587.00,1),(117,'I',5,4960.00,1),(118,'J',5,8980.00,1),(119,'K',5,3788.00,1),(120,'M',5,3905.00,1),(121,'U',5,4602.00,1),(122,'A',5,6961.00,1),(123,'D',5,13626.00,1),(124,'E',5,4591.00,1),(125,'F',5,4652.00,1),(126,'G',5,12215.00,1),(127,'H',5,4926.00,1),(128,'I',5,5366.00,1),(129,'J',5,9734.00,1),(130,'K',5,3997.00,1),(131,'M',5,4194.00,1),(132,'U',5,4882.00,1),(133,'A',6,6964.00,1),(134,'D',6,14988.00,1),(135,'E',6,5560.00,1),(136,'F',6,5648.00,1),(137,'G',6,14485.00,1),(138,'H',6,5951.00,1),(139,'I',6,6788.00,1),(140,'J',6,12853.00,1),(141,'K',6,4018.00,1),(142,'M',6,4880.00,1),(143,'U',6,5086.00,1),(144,'A',6,7233.00,1),(145,'D',6,15830.00,1),(146,'E',6,5737.00,1),(147,'F',6,5828.00,1),(148,'G',6,14884.00,1),(149,'H',6,6196.00,1),(150,'I',6,6984.00,1),(151,'J',6,13386.00,1),(152,'K',6,4173.00,1),(153,'M',6,5081.00,1),(154,'U',6,5372.00,1),(155,'A',7,7503.00,1),(156,'D',7,16671.00,1),(157,'E',7,5914.00,1),(158,'F',7,6009.00,1),(159,'G',7,15283.00,1),(160,'H',7,6441.00,1),(161,'I',7,7178.00,1),(162,'J',7,13921.00,1),(163,'K',7,4329.00,1),(164,'M',7,5283.00,1),(165,'U',7,5657.00,1),(166,'A',7,7772.00,1),(167,'D',7,17512.00,1),(168,'E',7,6090.00,1),(169,'F',7,6189.00,1),(170,'G',7,15682.00,1),(171,'H',7,6686.00,1),(172,'I',7,7374.00,1),(173,'J',7,14455.00,1),(174,'K',7,4484.00,1),(175,'M',7,5483.00,1),(176,'U',7,5942.00,1),(177,'A',8,8041.00,1),(178,'D',8,18354.00,1),(179,'E',8,6267.00,1),(180,'F',8,6369.00,1),(181,'G',8,16082.00,1),(182,'H',8,6931.00,1),(183,'I',8,7569.00,1),(184,'J',8,14990.00,1),(185,'K',8,4639.00,1),(186,'M',8,5684.00,1),(187,'U',8,6229.00,1),(188,'A',8,8311.00,1),(189,'D',8,19194.00,1),(190,'E',8,6444.00,1),(191,'F',8,6549.00,1),(192,'G',8,16481.00,1),(193,'H',8,7177.00,1),(194,'I',8,7764.00,1),(195,'J',8,15523.00,1),(196,'K',8,4794.00,1),(197,'M',8,5885.00,1),(198,'U',8,6514.00,1),(199,'A',9,8580.00,1),(200,'D',9,20036.00,1),(201,'E',9,6621.00,1),(202,'F',9,6729.00,1),(203,'G',9,16880.00,1),(204,'H',9,7422.00,1),(205,'I',9,7960.00,1),(206,'J',9,16058.00,1),(207,'K',9,4950.00,1),(208,'M',9,6086.00,1),(209,'U',9,6799.00,1),(210,'A',9,8849.00,1),(211,'D',9,20877.00,1),(212,'E',9,6797.00,1),(213,'F',9,6910.00,1),(214,'G',9,17279.00,1),(215,'H',9,7667.00,1),(216,'I',9,8155.00,1),(217,'J',9,16592.00,1),(218,'K',9,5106.00,1),(219,'M',9,6288.00,1),(220,'U',9,7085.00,1),(221,'A',10,8889.00,1),(222,'D',10,21089.00,1),(223,'E',10,8327.00,1),(224,'F',10,8450.00,1),(225,'G',10,20886.00,1),(226,'H',10,9328.00,1),(227,'I',10,10130.00,1),(228,'J',10,20041.00,1),(229,'K',10,5261.00,1),(230,'M',10,7634.00,1),(231,'U',10,8041.00,1),(232,'A',10,9152.00,1),(233,'D',10,21905.00,1),(234,'E',10,8539.00,1),(235,'F',10,8665.00,1),(236,'G',10,21358.00,1),(237,'H',10,9618.00,1),(238,'I',10,10367.00,1),(239,'J',10,20665.00,1),(240,'K',10,5417.00,1),(241,'M',10,7870.00,1),(242,'U',10,8351.00,1),(243,'A',11,9386.00,1),(244,'D',11,22565.00,1),(245,'E',11,8765.00,1),(246,'F',11,8910.00,1),(247,'G',11,21886.00,1),(248,'H',11,9816.00,1),(249,'I',11,10628.00,1),(250,'J',11,21466.00,1),(251,'K',11,5556.00,1),(252,'M',11,8031.00,1),(253,'U',11,8604.00,1),(254,'A',11,9622.00,1),(255,'D',11,23226.00,1),(256,'E',11,8991.00,1),(257,'F',11,9155.00,1),(258,'G',11,22415.00,1),(259,'H',11,10013.00,1),(260,'I',11,10888.00,1),(261,'J',11,22268.00,1),(262,'K',11,5695.00,1),(263,'M',11,8193.00,1),(264,'U',11,8855.00,1),(265,'A',12,9857.00,1),(266,'D',12,23885.00,1),(267,'E',12,9217.00,1),(268,'F',12,9401.00,1),(269,'G',12,22943.00,1),(270,'H',12,10211.00,1),(271,'I',12,11149.00,1),(272,'J',12,23069.00,1),(273,'K',12,5834.00,1),(274,'M',12,8355.00,1),(275,'U',12,9107.00,1),(276,'A',12,10092.00,1),(277,'D',12,24545.00,1),(278,'E',12,9444.00,1),(279,'F',12,9645.00,1),(280,'G',12,23471.00,1),(281,'H',12,10408.00,1),(282,'I',12,11409.00,1),(283,'J',12,23870.00,1),(284,'K',12,5973.00,1),(285,'M',12,8516.00,1),(286,'U',12,9358.00,1);
/*!40000 ALTER TABLE `m_shipping` ENABLE KEYS */;

--
-- Table structure for table `m_shipping_surcharge`
--

DROP TABLE IF EXISTS `m_shipping_surcharge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_shipping_surcharge` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `surcharge_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `rate` decimal(5,2) NOT NULL,
  `fixed_amount` decimal(10,2) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `service_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `m_shipping_surcharge_service_id_adc8f13b_fk_m_service_id` (`service_id`),
  CONSTRAINT `m_shipping_surcharge_service_id_adc8f13b_fk_m_service_id` FOREIGN KEY (`service_id`) REFERENCES `m_service` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `m_shipping_surcharge`
--

/*!40000 ALTER TABLE `m_shipping_surcharge` DISABLE KEYS */;
/*!40000 ALTER TABLE `m_shipping_surcharge` ENABLE KEYS */;

--
-- Table structure for table `m_status`
--

DROP TABLE IF EXISTS `m_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_status` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `m_status`
--

/*!40000 ALTER TABLE `m_status` DISABLE KEYS */;
INSERT INTO `m_status` VALUES (1,'出品中'),(2,'取下げ'),(3,'売却'),(4,'完了'),(5,'出品失敗');
/*!40000 ALTER TABLE `m_status` ENABLE KEYS */;

--
-- Table structure for table `m_tax`
--

DROP TABLE IF EXISTS `m_tax`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_tax` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rate` decimal(4,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `m_tax`
--

/*!40000 ALTER TABLE `m_tax` DISABLE KEYS */;
INSERT INTO `m_tax` VALUES (1,10.00),(2,8.00);
/*!40000 ALTER TABLE `m_tax` ENABLE KEYS */;

--
-- Table structure for table `m_yahoo_auction_status`
--

DROP TABLE IF EXISTS `m_yahoo_auction_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_yahoo_auction_status` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `m_yahoo_auction_status`
--

/*!40000 ALTER TABLE `m_yahoo_auction_status` DISABLE KEYS */;
INSERT INTO `m_yahoo_auction_status` VALUES (1,'購入可'),(2,'購入済'),(3,'購入不可');
/*!40000 ALTER TABLE `m_yahoo_auction_status` ENABLE KEYS */;

--
-- Table structure for table `m_yahoo_free_market_status`
--

DROP TABLE IF EXISTS `m_yahoo_free_market_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `m_yahoo_free_market_status` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `m_yahoo_free_market_status`
--

/*!40000 ALTER TABLE `m_yahoo_free_market_status` DISABLE KEYS */;
INSERT INTO `m_yahoo_free_market_status` VALUES (1,'購入可'),(2,'購入済'),(3,'購入不可');
/*!40000 ALTER TABLE `m_yahoo_free_market_status` ENABLE KEYS */;

--
-- Table structure for table `oauth2_provider_accesstoken`
--

DROP TABLE IF EXISTS `oauth2_provider_accesstoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oauth2_provider_accesstoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires` datetime(6) NOT NULL,
  `scope` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `application_id` bigint DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `source_refresh_token_id` bigint DEFAULT NULL,
  `id_token_id` bigint DEFAULT NULL,
  `token_checksum` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `oauth2_provider_accesstoken_token_checksum_85319a26_uniq` (`token_checksum`),
  UNIQUE KEY `source_refresh_token_id` (`source_refresh_token_id`),
  UNIQUE KEY `id_token_id` (`id_token_id`),
  KEY `oauth2_provider_acce_application_id_b22886e1_fk_oauth2_pr` (`application_id`),
  KEY `oauth2_provider_accesstoken_user_id_6e4c9a65_fk_users_id` (`user_id`),
  CONSTRAINT `oauth2_provider_acce_application_id_b22886e1_fk_oauth2_pr` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`),
  CONSTRAINT `oauth2_provider_acce_id_token_id_85db651b_fk_oauth2_pr` FOREIGN KEY (`id_token_id`) REFERENCES `oauth2_provider_idtoken` (`id`),
  CONSTRAINT `oauth2_provider_acce_source_refresh_token_e66fbc72_fk_oauth2_pr` FOREIGN KEY (`source_refresh_token_id`) REFERENCES `oauth2_provider_refreshtoken` (`id`),
  CONSTRAINT `oauth2_provider_accesstoken_user_id_6e4c9a65_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_provider_accesstoken`
--

/*!40000 ALTER TABLE `oauth2_provider_accesstoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth2_provider_accesstoken` ENABLE KEYS */;

--
-- Table structure for table `oauth2_provider_application`
--

DROP TABLE IF EXISTS `oauth2_provider_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oauth2_provider_application` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `client_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `redirect_uris` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `client_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `authorization_grant_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `client_secret` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `skip_authorization` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `algorithm` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_logout_redirect_uris` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  `hash_client_secret` tinyint(1) NOT NULL,
  `allowed_origins` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  PRIMARY KEY (`id`),
  UNIQUE KEY `client_id` (`client_id`),
  KEY `oauth2_provider_application_user_id_79829054_fk_users_id` (`user_id`),
  KEY `oauth2_provider_application_client_secret_53133678` (`client_secret`),
  CONSTRAINT `oauth2_provider_application_user_id_79829054_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_provider_application`
--

/*!40000 ALTER TABLE `oauth2_provider_application` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth2_provider_application` ENABLE KEYS */;

--
-- Table structure for table `oauth2_provider_grant`
--

DROP TABLE IF EXISTS `oauth2_provider_grant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oauth2_provider_grant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires` datetime(6) NOT NULL,
  `redirect_uri` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `scope` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `application_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `code_challenge` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `code_challenge_method` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `nonce` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `claims` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `oauth2_provider_gran_application_id_81923564_fk_oauth2_pr` (`application_id`),
  KEY `oauth2_provider_grant_user_id_e8f62af8_fk_users_id` (`user_id`),
  CONSTRAINT `oauth2_provider_gran_application_id_81923564_fk_oauth2_pr` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`),
  CONSTRAINT `oauth2_provider_grant_user_id_e8f62af8_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_provider_grant`
--

/*!40000 ALTER TABLE `oauth2_provider_grant` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth2_provider_grant` ENABLE KEYS */;

--
-- Table structure for table `oauth2_provider_idtoken`
--

DROP TABLE IF EXISTS `oauth2_provider_idtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oauth2_provider_idtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `jti` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires` datetime(6) NOT NULL,
  `scope` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `application_id` bigint DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `jti` (`jti`),
  KEY `oauth2_provider_idto_application_id_08c5ff4f_fk_oauth2_pr` (`application_id`),
  KEY `oauth2_provider_idtoken_user_id_dd512b59_fk_users_id` (`user_id`),
  CONSTRAINT `oauth2_provider_idto_application_id_08c5ff4f_fk_oauth2_pr` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`),
  CONSTRAINT `oauth2_provider_idtoken_user_id_dd512b59_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_provider_idtoken`
--

/*!40000 ALTER TABLE `oauth2_provider_idtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth2_provider_idtoken` ENABLE KEYS */;

--
-- Table structure for table `oauth2_provider_refreshtoken`
--

DROP TABLE IF EXISTS `oauth2_provider_refreshtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oauth2_provider_refreshtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `access_token_id` bigint DEFAULT NULL,
  `application_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `revoked` datetime(6) DEFAULT NULL,
  `token_family` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `access_token_id` (`access_token_id`),
  UNIQUE KEY `oauth2_provider_refreshtoken_token_revoked_af8a5134_uniq` (`token`,`revoked`),
  KEY `oauth2_provider_refr_application_id_2d1c311b_fk_oauth2_pr` (`application_id`),
  KEY `oauth2_provider_refreshtoken_user_id_da837fce_fk_users_id` (`user_id`),
  CONSTRAINT `oauth2_provider_refr_access_token_id_775e84e8_fk_oauth2_pr` FOREIGN KEY (`access_token_id`) REFERENCES `oauth2_provider_accesstoken` (`id`),
  CONSTRAINT `oauth2_provider_refr_application_id_2d1c311b_fk_oauth2_pr` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`),
  CONSTRAINT `oauth2_provider_refreshtoken_user_id_da837fce_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_provider_refreshtoken`
--

/*!40000 ALTER TABLE `oauth2_provider_refreshtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth2_provider_refreshtoken` ENABLE KEYS */;

--
-- Table structure for table `social_auth_association`
--

DROP TABLE IF EXISTS `social_auth_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `social_auth_association` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `handle` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `secret` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `issued` int NOT NULL,
  `lifetime` int NOT NULL,
  `assoc_type` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_association_server_url_handle_078befa2_uniq` (`server_url`,`handle`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_association`
--

/*!40000 ALTER TABLE `social_auth_association` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_association` ENABLE KEYS */;

--
-- Table structure for table `social_auth_code`
--

DROP TABLE IF EXISTS `social_auth_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `social_auth_code` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_code_email_code_801b2d02_uniq` (`email`,`code`),
  KEY `social_auth_code_code_a2393167` (`code`),
  KEY `social_auth_code_timestamp_176b341f` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_code`
--

/*!40000 ALTER TABLE `social_auth_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_code` ENABLE KEYS */;

--
-- Table structure for table `social_auth_nonce`
--

DROP TABLE IF EXISTS `social_auth_nonce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `social_auth_nonce` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` int NOT NULL,
  `salt` varchar(65) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_nonce_server_url_timestamp_salt_f6284463_uniq` (`server_url`,`timestamp`,`salt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_nonce`
--

/*!40000 ALTER TABLE `social_auth_nonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_nonce` ENABLE KEYS */;

--
-- Table structure for table `social_auth_partial`
--

DROP TABLE IF EXISTS `social_auth_partial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `social_auth_partial` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `next_step` smallint unsigned NOT NULL,
  `backend` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `data` json NOT NULL DEFAULT (_utf8mb3'{}'),
  PRIMARY KEY (`id`),
  KEY `social_auth_partial_token_3017fea3` (`token`),
  KEY `social_auth_partial_timestamp_50f2119f` (`timestamp`),
  CONSTRAINT `social_auth_partial_chk_1` CHECK ((`next_step` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_partial`
--

/*!40000 ALTER TABLE `social_auth_partial` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_partial` ENABLE KEYS */;

--
-- Table structure for table `social_auth_usersocialauth`
--

DROP TABLE IF EXISTS `social_auth_usersocialauth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `social_auth_usersocialauth` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `provider` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `uid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint NOT NULL,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `extra_data` json NOT NULL DEFAULT (_utf8mb3'{}'),
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_usersocialauth_provider_uid_e6b5e668_uniq` (`provider`,`uid`),
  KEY `social_auth_usersocialauth_user_id_17d28448_fk_users_id` (`user_id`),
  KEY `social_auth_usersocialauth_uid_796e51dc` (`uid`),
  CONSTRAINT `social_auth_usersocialauth_user_id_17d28448_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_usersocialauth`
--

/*!40000 ALTER TABLE `social_auth_usersocialauth` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_usersocialauth` ENABLE KEYS */;

--
-- Table structure for table `t_ebay`
--

DROP TABLE IF EXISTS `t_ebay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_ebay` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sku` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `offer_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `shipping_price` decimal(10,2) NOT NULL,
  `final_profit` decimal(10,2) NOT NULL,
  `update_datetime` datetime(6) NOT NULL,
  `insert_datetime` datetime(6) NOT NULL,
  `status_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `yahoo_auction_id_id` bigint DEFAULT NULL,
  `yahoo_free_market_id_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku` (`sku`),
  KEY `t_ebay_sku_a442ba_idx` (`sku`),
  KEY `t_ebay_status__0fecaf_idx` (`status_id`),
  KEY `ebay_user_id_1570f82a_fk_users_id` (`user_id`),
  KEY `ebay_yahoo_auction_id_id_7d070aa3_fk_yahoo_auction_id` (`yahoo_auction_id_id`),
  KEY `ebay_yahoo_free_market_id_id_081f4517_fk_yahoo_free_market_id` (`yahoo_free_market_id_id`),
  CONSTRAINT `ebay_status_id_63fe192b_fk_m_status_id` FOREIGN KEY (`status_id`) REFERENCES `m_status` (`id`),
  CONSTRAINT `ebay_user_id_1570f82a_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `ebay_yahoo_auction_id_id_7d070aa3_fk_yahoo_auction_id` FOREIGN KEY (`yahoo_auction_id_id`) REFERENCES `t_yahoo_auction` (`id`),
  CONSTRAINT `ebay_yahoo_free_market_id_id_081f4517_fk_yahoo_free_market_id` FOREIGN KEY (`yahoo_free_market_id_id`) REFERENCES `t_yahoo_free_market` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_ebay`
--

/*!40000 ALTER TABLE `t_ebay` DISABLE KEYS */;
INSERT INTO `t_ebay` VALUES (1,'YFM_z411631248_20250227032247','40640195011',137.00,3000.00,21.00,'2025-02-26 18:22:51.703905','2025-02-26 18:22:51.703905',1,5,NULL,6),(2,'YFM_z409646368_20250227033919','40640529011',139.00,3000.00,21.00,'2025-02-26 18:39:24.250342','2025-02-26 18:39:24.250342',1,5,NULL,7),(3,'YFM_z412947946_20250227040110','40641129011',190.00,3000.00,21.00,'2025-02-26 19:01:15.626660','2025-02-26 19:01:15.626660',1,5,NULL,8),(4,'YFM_z413034808_20250227041319','40641396011',300.00,3000.00,147.00,'2025-02-26 19:13:24.333684','2025-02-26 19:13:24.333684',1,5,NULL,9),(5,'YFM_z412040278_20250227043057','40641742011',250.00,3000.00,72.00,'2025-02-26 19:31:02.428721','2025-02-26 19:31:02.428721',1,5,NULL,10),(6,'YFM_z411739018_20250227095742','40649970011',130.00,3000.00,17.00,'2025-02-27 00:57:46.820244','2025-02-27 00:57:46.820244',1,5,NULL,11),(7,'YFM_z381060748_20250227144300','40656322011',100.00,3000.00,33.00,'2025-02-27 05:43:05.653533','2025-02-27 05:43:05.653533',1,5,NULL,12),(8,'YFM_z396639448_20250227151631','40656590011',345.00,3000.00,17.00,'2025-02-27 06:16:36.673478','2025-02-27 06:16:36.673478',1,5,NULL,13),(9,'YFM_z412897280_20250227180606','40658767011',262.00,3000.00,33.00,'2025-02-27 15:52:28.187410','2025-02-27 09:06:10.452124',2,5,NULL,14),(10,'YFM_z412063094_20250227194615','40670863011',267.00,3000.00,33.00,'2025-02-27 10:46:19.426485','2025-02-27 10:46:19.426485',1,5,NULL,15),(11,'YFM_z404895800_20250227215949','40698890011',154.00,3000.00,19.00,'2025-02-27 12:59:54.628021','2025-02-27 12:59:54.628021',1,5,NULL,16),(12,'YA_q1173163215_20250227221209','40701953011',208.00,3000.00,26.00,'2025-02-27 13:12:13.012376','2025-02-27 13:12:13.012376',1,5,3,NULL);
/*!40000 ALTER TABLE `t_ebay` ENABLE KEYS */;

--
-- Table structure for table `t_yahoo_auction`
--

DROP TABLE IF EXISTS `t_yahoo_auction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_yahoo_auction` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `unique_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `item_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `item_price` decimal(10,2) NOT NULL,
  `shipping` decimal(10,2) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `update_datetime` datetime(6) NOT NULL,
  `insert_datetime` datetime(6) NOT NULL,
  `status_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `t_yahoo_auc_status__b71c32_idx` (`status_id`),
  KEY `yahoo_auction_user_id_1a691297_fk_users_id` (`user_id`),
  CONSTRAINT `yahoo_auction_status_id_60e9016e_fk_m_yahoo_auction_status_id` FOREIGN KEY (`status_id`) REFERENCES `m_yahoo_auction_status` (`id`),
  CONSTRAINT `yahoo_auction_user_id_1a691297_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_yahoo_auction`
--

/*!40000 ALTER TABLE `t_yahoo_auction` DISABLE KEYS */;
INSERT INTO `t_yahoo_auction` VALUES (3,'q1173163215','https://page.auctions.yahoo.co.jp/jp/auction/q1173163215','Nikon AF-S NIKKOR 24-85mm f/3.5-4.5 G ED IF [美品] レンズポーチ 前後キャップ付き 標準ズームレンズ',19280.00,0.00,'2025-03-06 23:52:00.000000','2025-02-27 13:12:13.002369','2025-02-27 13:12:13.002369',1,5);
/*!40000 ALTER TABLE `t_yahoo_auction` ENABLE KEYS */;

--
-- Table structure for table `t_yahoo_free_market`
--

DROP TABLE IF EXISTS `t_yahoo_free_market`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_yahoo_free_market` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `unique_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `item_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `item_price` decimal(10,2) NOT NULL,
  `shipping` decimal(10,2) NOT NULL,
  `update_datetime` datetime(6) NOT NULL,
  `insert_datetime` datetime(6) NOT NULL,
  `status_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `t_yahoo_fre_status__0842a1_idx` (`status_id`),
  KEY `yahoo_free_market_user_id_a4c2e7ea_fk_users_id` (`user_id`),
  CONSTRAINT `t_yahoo_free_market_status_id_07cb86f9_fk_m_yahoo_f` FOREIGN KEY (`status_id`) REFERENCES `m_yahoo_free_market_status` (`id`),
  CONSTRAINT `yahoo_free_market_user_id_a4c2e7ea_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_yahoo_free_market`
--

/*!40000 ALTER TABLE `t_yahoo_free_market` DISABLE KEYS */;
INSERT INTO `t_yahoo_free_market` VALUES (6,'z411631248','https://paypayfleamarket.yahoo.co.jp/item/z411631248','動作品 PENTAX optio I-10 ブラック ペンタックス オールドコンデジ  デジタルカメラ',11000.00,0.00,'2025-02-26 18:22:51.696621','2025-02-26 18:22:51.696621',1,5),(7,'z409646368','https://paypayfleamarket.yahoo.co.jp/item/z409646368','【動作確認済】Nikon ニコン COOLPIX S520 レトロコンデジ ピンク デジタルカメラ コンデジ',11180.00,0.00,'2025-02-26 18:39:24.244833','2025-02-26 18:39:24.244833',1,5),(8,'z412947946','https://paypayfleamarket.yahoo.co.jp/item/z412947946','PowerShot SX200 IS コンパクトデジタルカメラ',18000.00,0.00,'2025-02-26 19:01:15.617686','2025-02-26 19:01:15.617686',1,5),(9,'z413034808','https://paypayfleamarket.yahoo.co.jp/item/z413034808',' CASIO EXILIM デジタルカメラ',13000.00,0.00,'2025-02-26 19:13:24.328268','2025-02-26 19:13:24.328268',1,5),(10,'z412040278','https://paypayfleamarket.yahoo.co.jp/item/z412040278','Nikon ニコン 美品 デジタル一眼レフカメラ 本体 D80 18-135 レンズ バッテリー2個 充電器 ストラップ2個付き',18000.00,0.00,'2025-02-26 19:31:02.424192','2025-02-26 19:31:02.424192',1,5),(11,'z411739018','https://paypayfleamarket.yahoo.co.jp/item/z411739018','Panasonic パナソニック LUMIX デジカメ コンパクトデジタルカメラ ルミックス コンデジ  DMC-FX60 ピンク',11000.00,0.00,'2025-02-27 00:57:46.811243','2025-02-27 00:57:46.811243',1,5),(12,'z381060748','https://paypayfleamarket.yahoo.co.jp/item/z381060748','PENTAX Super TAKMAR 200mm F4',4750.00,0.00,'2025-02-27 05:43:05.632347','2025-02-27 05:43:05.632347',1,5),(13,'z396639448','https://paypayfleamarket.yahoo.co.jp/item/z396639448','美品！ オリンパス OLYMPUS STYLUS 1s コンパクトデジタルカメラ ',38500.00,0.00,'2025-02-27 06:16:36.664275','2025-02-27 06:16:36.664275',1,5),(14,'z412897280','https://paypayfleamarket.yahoo.co.jp/item/z412897280','OLYMPUS Tough TG-5 タフカメラ　防水カメラ',25000.00,0.00,'2025-02-27 15:52:28.200396','2025-02-27 09:06:10.435255',3,5),(15,'z412063094','https://paypayfleamarket.yahoo.co.jp/item/z412063094','美品 SONY FE 50mm F1.8 SEL50F18F 単焦点レンズ　フルサイズ　ソニーEマウント',25500.00,0.00,'2025-02-27 10:46:19.408139','2025-02-27 10:46:19.409139',1,5),(16,'z404895800','https://paypayfleamarket.yahoo.co.jp/item/z404895800','【即購入で1000円OFF!】超望遠レンズ★Canon EF 75-300㎜ Ⅲ★スポーツ 鉄道 発表会 進学 キャノン',13499.00,0.00,'2025-02-27 12:59:54.623025','2025-02-27 12:59:54.623025',1,5);
/*!40000 ALTER TABLE `t_yahoo_free_market` ENABLE KEYS */;

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_blacklistedtoken`
--

/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` DISABLE KEYS */;
INSERT INTO `token_blacklist_blacklistedtoken` VALUES (1,'2025-02-11 19:10:33.903344',46),(2,'2025-02-11 19:11:02.070184',48),(3,'2025-02-12 12:59:14.882234',51),(4,'2025-02-13 08:51:11.303652',60),(5,'2025-02-13 13:43:05.197645',65),(6,'2025-02-13 13:43:05.212773',66),(7,'2025-02-13 13:52:18.237886',68),(8,'2025-02-13 13:59:35.120014',70),(9,'2025-02-26 15:41:27.035100',146),(10,'2025-02-27 04:36:46.770408',154),(11,'2025-02-27 04:59:07.104758',160);
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` ENABLE KEYS */;

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `jti` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outstandingtoken_user_id_83bc629a_fk_users_id` (`user_id`),
  CONSTRAINT `token_blacklist_outstandingtoken_user_id_83bc629a_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=175 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` DISABLE KEYS */;
INSERT INTO `token_blacklist_outstandingtoken` VALUES (1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTc4NjUyMiwiaWF0IjoxNzM5MTgxNzIyLCJqdGkiOiJkNDA5MDk4NDYzMTE0YWY2YjYwNDFmYWE2Zjg0M2Q1YSIsInVzZXJfaWQiOjV9.XslI3Rb28YyGLa_0pAjxUmKuuFdu-DEQBFMAjqTKdps','2025-02-10 10:02:02.289902','2025-02-17 10:02:02.000000',5,'d409098463114af6b6041faa6f843d5a'),(2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgwMjE2NywiaWF0IjoxNzM5MTk3MzY3LCJqdGkiOiIwZGQ5MjkxODZlZWQ0ZGU3YjUxODRkMDVmNjZkMWI0MCIsInVzZXJfaWQiOjV9.kMjMDt5gLq-XOAskJMaDWyq2Lqu7-5BM9sJdvL91FN4','2025-02-10 14:22:47.671378','2025-02-17 14:22:47.000000',5,'0dd929186eed4de7b5184d05f66d1b40'),(3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgwMjI1NSwiaWF0IjoxNzM5MTk3NDU1LCJqdGkiOiI2NTExYjFlMGFiNDk0NTRiYTIyYTc5YmM0YWJiYjI5MSIsInVzZXJfaWQiOjV9.IRW6hd-OdDYuRBeXSv3m8gBbkB0LSXFejRDxCtM-QVU','2025-02-10 14:24:15.140164','2025-02-17 14:24:15.000000',5,'6511b1e0ab49454ba22a79bc4abbb291'),(4,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgwNjY5NywiaWF0IjoxNzM5MjAxODk3LCJqdGkiOiIwYTk1YzVkZDA0Yzc0OTY4YmMyMjhjYWI1MDYwZWY5YiIsInVzZXJfaWQiOjV9.uCv4Fn9WxHjSqH3Pkc8HkfhL4-Ro-Ewjbno0bLThtCY','2025-02-10 15:38:17.703378','2025-02-17 15:38:17.000000',5,'0a95c5dd04c74968bc228cab5060ef9b'),(5,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgwNjcyMSwiaWF0IjoxNzM5MjAxOTIxLCJqdGkiOiI0NGJlODE5OWQyODE0NjQ0OTYyOTBlMmYzMGM3OTA3MyIsInVzZXJfaWQiOjV9.07YCRanYcL5r4T9R9kOjiW2z8MqkOKABapHQeyi1_FQ','2025-02-10 15:38:41.523192','2025-02-17 15:38:41.000000',5,'44be8199d281464496290e2f30c79073'),(6,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgwNjc3MiwiaWF0IjoxNzM5MjAxOTcyLCJqdGkiOiI2MWY4NDY0MzNiMjc0MGM2OWFiNmFjZWI3N2M1N2M1MCIsInVzZXJfaWQiOjV9.ACEX3Ou-0-oGNgH8PXGr3CoNRUUA_cFjLl2-WOzEROI','2025-02-10 15:39:32.375406','2025-02-17 15:39:32.000000',5,'61f846433b2740c69ab6aceb77c57c50'),(7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgwNjc3OSwiaWF0IjoxNzM5MjAxOTc5LCJqdGkiOiI0ZTYyODI4MWFiZjM0NzkzYWM3MDQwYjM1MDdlYTkxZCIsInVzZXJfaWQiOjV9.dAZwjzb3khUsrecdSCLU4YzRMgeu7vkbg0Qws6lR6JQ','2025-02-10 15:39:39.287429','2025-02-17 15:39:39.000000',5,'4e628281abf34793ac7040b3507ea91d'),(8,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgwNjkwMCwiaWF0IjoxNzM5MjAyMTAwLCJqdGkiOiIzZDI1YjE3NjE3NWM0ODRhOTRlYmNiZTIyZmMxNzhhOSIsInVzZXJfaWQiOjV9.dPqymbLrCr2q7AtWw-yTS_cOh9JyILToyG2jgDdE5gE','2025-02-10 15:41:40.311018','2025-02-17 15:41:40.000000',5,'3d25b176175c484a94ebcbe22fc178a9'),(9,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgwNjkzMSwiaWF0IjoxNzM5MjAyMTMxLCJqdGkiOiJhOTNhNDg3NjI4M2U0ZWExOTgzZjY4YjI3OWMwZGQ1NSIsInVzZXJfaWQiOjV9.B3hzl38SEoiFDcCOhFBhSso6IMEskmvPFuESUbM-g9M','2025-02-10 15:42:11.129591','2025-02-17 15:42:11.000000',5,'a93a4876283e4ea1983f68b279c0dd55'),(10,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgwNjk4NywiaWF0IjoxNzM5MjAyMTg3LCJqdGkiOiIwNDkyYjk1NWNjMjY0NmVjODdlYjUzOWQyNmNmMWZiYiIsInVzZXJfaWQiOjV9.QbPd3LfZtfhR11okMRkFE04t2TVJaLJ9wDe9sXrj774','2025-02-10 15:43:07.411273','2025-02-17 15:43:07.000000',5,'0492b955cc2646ec87eb539d26cf1fbb'),(11,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgwNzg5MSwiaWF0IjoxNzM5MjAzMDkxLCJqdGkiOiJmY2YxN2Y2M2IzYzI0OTQ2YTRiNDQyNjEyNzc0MGU1ZCIsInVzZXJfaWQiOjV9.mH3bMsKd1DOFsurz7YugFyywKM1tjT41qSK7xXCvORM','2025-02-10 15:58:11.433097','2025-02-17 15:58:11.000000',5,'fcf17f63b3c24946a4b4426127740e5d'),(12,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgxOTY0MCwiaWF0IjoxNzM5MjE0ODQwLCJqdGkiOiIzYWE4MzZkNmY5NGU0NmMzYTlmNDYzZjMxZTY5YWY2NyIsInVzZXJfaWQiOjV9.3iVbUUittCpjjEgxhY6tWvlUMKiV-49mUt6z0lZUG5k','2025-02-10 19:14:00.611472','2025-02-17 19:14:00.000000',5,'3aa836d6f94e46c3a9f463f31e69af67'),(13,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgxOTcxMiwiaWF0IjoxNzM5MjE0OTEyLCJqdGkiOiIxMTFmYjdhOWEzNjc0NDg3OWNiMjA1ZGUxNTIzYTgzNyIsInVzZXJfaWQiOjV9.f7hLPoqxYR7WzVaTX2ZB2TjJzW_ioNDHIPkVj4IavQU','2025-02-10 19:15:12.867335','2025-02-17 19:15:12.000000',5,'111fb7a9a36744879cb205de1523a837'),(14,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTMyMCwiaWF0IjoxNzM5MjE2NTIwLCJqdGkiOiJlMDQ3Y2EyYzM3OTk0MDA4OTZiNmJhYzM2MjhmNjVjNCIsInVzZXJfaWQiOjV9.z9hZDUzI9kbiNpv0EJWroTOeGLx9NrC-O0My_26a-6w','2025-02-10 19:42:00.139759','2025-02-17 19:42:00.000000',5,'e047ca2c3799400896b6bac3628f65c4'),(15,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTMzNSwiaWF0IjoxNzM5MjE2NTM1LCJqdGkiOiJiNjZhZWRiNjhhZDQ0ZWUwOThkMWM0MDk3MjZhYzg5MiIsInVzZXJfaWQiOjV9.hrqY6D5ExyZjWezV1BmRCgK_-0zTmzmzQfshNEm7O1s','2025-02-10 19:42:15.876360','2025-02-17 19:42:15.000000',5,'b66aedb68ad44ee098d1c409726ac892'),(16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTQ1NywiaWF0IjoxNzM5MjE2NjU3LCJqdGkiOiJlM2JjYjZiNThlOTY0NjkxOGYyNDc3MDE5NjQ3NDBlZiIsInVzZXJfaWQiOjV9.SvpyIdjJuYKtm8O7agWb3ZvRsa6qWdKrb7GhcKTcjNM','2025-02-10 19:44:17.416446','2025-02-17 19:44:17.000000',5,'e3bcb6b58e9646918f247701964740ef'),(17,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTY2MCwiaWF0IjoxNzM5MjE2ODYwLCJqdGkiOiIwYWI3OWQxNzI5NDM0NDQyYWY0YTczOGViY2RiODhkZCIsInVzZXJfaWQiOjV9.3TI3_TAcHbTxfhROzAQBsgPAbkoajEOvFvhrmUWD_Rk','2025-02-10 19:47:40.421656','2025-02-17 19:47:40.000000',5,'0ab79d1729434442af4a738ebcdb88dd'),(18,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTY3NCwiaWF0IjoxNzM5MjE2ODc0LCJqdGkiOiIxY2VkZDg1ZDA5NjU0NmYxYmY3ODRhYTlhNDI5M2E4YSIsInVzZXJfaWQiOjV9.n1Rf3KQz39epIVZumwSCc0hfpWoWlYisXmDklfXo34M','2025-02-10 19:47:54.045640','2025-02-17 19:47:54.000000',5,'1cedd85d096546f1bf784aa9a4293a8a'),(19,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTcyNSwiaWF0IjoxNzM5MjE2OTI1LCJqdGkiOiIwYTc1ZjVjMTRlODA0YmQxYWUxMzg3YmExYTVlMTIwZSIsInVzZXJfaWQiOjV9.4i6xVMcOzkb9qhJ7Pj_GLt0t3vDHXXEq-z84BF50wpY','2025-02-10 19:48:45.367522','2025-02-17 19:48:45.000000',5,'0a75f5c14e804bd1ae1387ba1a5e120e'),(20,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTc2NSwiaWF0IjoxNzM5MjE2OTY1LCJqdGkiOiJhNDJmYjk4NThlNGY0MjJlODcyMmZlYmZlYzc1MWY5ZCIsInVzZXJfaWQiOjV9.pRoWtUtyxK0TzSPRboFIPGVSTgyrXKNFCXkFf6-RSEk','2025-02-10 19:49:25.852062','2025-02-17 19:49:25.000000',5,'a42fb9858e4f422e8722febfec751f9d'),(21,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTc4NiwiaWF0IjoxNzM5MjE2OTg2LCJqdGkiOiIzMzFkOWI0YTA4NDE0ZjY2YmFlMDRlOTNmZGE0NGFlYiIsInVzZXJfaWQiOjV9.gII5uAOyYqXQIWqtHHZQ4hQSH9ZC9G_5lpFh2Jp4c0A','2025-02-10 19:49:46.787999','2025-02-17 19:49:46.000000',5,'331d9b4a08414f66bae04e93fda44aeb'),(22,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTgwNiwiaWF0IjoxNzM5MjE3MDA2LCJqdGkiOiJmYTkwOTQ3N2YxNmE0NWQwYWI3YTM0Yzg3ZjlkMTc1MiIsInVzZXJfaWQiOjV9.y55wthbu_rH3XGRqdS1IY91hYh20zCmJrZ_BQowPomw','2025-02-10 19:50:06.600973','2025-02-17 19:50:06.000000',5,'fa909477f16a45d0ab7a34c87f9d1752'),(23,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTgxNywiaWF0IjoxNzM5MjE3MDE3LCJqdGkiOiIxYjQzMzQ1MmNlNzI0YmViYjM1YzA3NmJhNzUzNTliNiIsInVzZXJfaWQiOjV9.48zaUZ_uECd7YouuvI16oL0XyQi4cjR7wpe8aoIfujY','2025-02-10 19:50:17.784001','2025-02-17 19:50:17.000000',5,'1b433452ce724bebb35c076ba75359b6'),(24,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTgzNiwiaWF0IjoxNzM5MjE3MDM2LCJqdGkiOiI2OGY5YTU0NzQ5MDE0OTY3YTFkY2FmODVhZTc2OTdkOCIsInVzZXJfaWQiOjV9.4-f9kTZEYFfhRpTBogxfeROVtUTx90qHb9hbz84hhEM','2025-02-10 19:50:36.998786','2025-02-17 19:50:36.000000',5,'68f9a54749014967a1dcaf85ae7697d8'),(25,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTg4OSwiaWF0IjoxNzM5MjE3MDg5LCJqdGkiOiJlNDE1M2Y1Y2UwYjI0OWIzOGMzMWE5OGE2YTdjMTUyYiIsInVzZXJfaWQiOjV9.OKVOdlUTCGA2xbLcU_vl4xkMAhEfmDckdwAJDqiOvbM','2025-02-10 19:51:29.186767','2025-02-17 19:51:29.000000',5,'e4153f5ce0b249b38c31a98a6a7c152b'),(26,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTkwMSwiaWF0IjoxNzM5MjE3MTAxLCJqdGkiOiIyZjA1NjY1NjA3OGI0YWM0YTc0NjFhOTM5ZGVkY2ExZSIsInVzZXJfaWQiOjV9.dxIaTeMq3yq2A0O-cKO_Gdhf3mvV7BQEGS0FAsTIoII','2025-02-10 19:51:41.927388','2025-02-17 19:51:41.000000',5,'2f056656078b4ac4a7461a939dedca1e'),(27,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTkxOSwiaWF0IjoxNzM5MjE3MTE5LCJqdGkiOiJiODZkMjNjZDAzYjc0MTA2YmE5YmI4NDY0NzI2MzFjYyIsInVzZXJfaWQiOjV9.-xs72JuIyWsyZ5WN7LBhU7Ke5g_N80GYablgWCtsCkc','2025-02-10 19:51:59.752853','2025-02-17 19:51:59.000000',5,'b86d23cd03b74106ba9bb846472631cc'),(28,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTkyNSwiaWF0IjoxNzM5MjE3MTI1LCJqdGkiOiI4NjIwODE2MWU4MzE0ZmRlYmRmMjZmMjA2MjhmNjYzMCIsInVzZXJfaWQiOjV9.SWimfyjFeA1nY8JQolOyazTpIK1rALLa6DvXGVzuD_c','2025-02-10 19:52:05.237770','2025-02-17 19:52:05.000000',5,'86208161e8314fdebdf26f20628f6630'),(29,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMTk1MiwiaWF0IjoxNzM5MjE3MTUyLCJqdGkiOiJmOTc5NWJlMTAyMDM0Y2NmYmZlODk5NjE2ZWY4MWMyMiIsInVzZXJfaWQiOjV9.Sdr_ZNXDdlWPCSpign9D1HInFvIacbf2z67Soyd3bAk','2025-02-10 19:52:32.837779','2025-02-17 19:52:32.000000',5,'f9795be102034ccfbfe899616ef81c22'),(30,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMjA3OCwiaWF0IjoxNzM5MjE3Mjc4LCJqdGkiOiIxODIwMzkzYjRkNGM0NGEyOWI3MDBmNGY3ZjU5MWM4OCIsInVzZXJfaWQiOjV9.54WajiJdzCMkYbW9EoyvpmMhXL_5EGMNQItPHfOw4jw','2025-02-10 19:54:38.015435','2025-02-17 19:54:38.000000',5,'1820393b4d4c44a29b700f4f7f591c88'),(31,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMjA5MSwiaWF0IjoxNzM5MjE3MjkxLCJqdGkiOiI1ZDgwMjA5ZjgwMWM0YTY3YTM0NTRjMDAwNjNmOTRlYSIsInVzZXJfaWQiOjV9.Lmlk_XBrWq5YriTiPPC98T60_fkDpdaLUMs-KB-w6v0','2025-02-10 19:54:51.055105','2025-02-17 19:54:51.000000',5,'5d80209f801c4a67a3454c00063f94ea'),(32,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMjExNSwiaWF0IjoxNzM5MjE3MzE1LCJqdGkiOiI5MDY1OGY3Y2U3MTc0OWNjODFmOGIwZGE0MTI2ZWVjNiIsInVzZXJfaWQiOjV9.yMbAX5uXjJdSvQcJ-wZM8-Dm2xkQ0zlRkGP-pJfaFZo','2025-02-10 19:55:15.240538','2025-02-17 19:55:15.000000',5,'90658f7ce71749cc81f8b0da4126eec6'),(33,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTgyMjM0NywiaWF0IjoxNzM5MjE3NTQ3LCJqdGkiOiI0NzA4NDM2M2JhZTc0NmRkODdmMjUyNDY5MzJjMDQwZCIsInVzZXJfaWQiOjV9.ievONbFGQdL2EixBDk_-Q9f393Ar7hwW-4-ENEv4Zxw','2025-02-10 19:59:07.767698','2025-02-17 19:59:07.000000',5,'47084363bae746dd87f25246932c040d'),(34,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTg3NzUzMiwiaWF0IjoxNzM5MjcyNzMyLCJqdGkiOiJkN2YzYjllZDEyZTc0ZDBiOWEwMjU3NDY5YTEzZjMxMSIsInVzZXJfaWQiOjV9.bMLxV3SRzM6idKiaYvBpCGHQVoUB39wdCwdkNlCRLWw','2025-02-11 11:18:52.481571','2025-02-18 11:18:52.000000',5,'d7f3b9ed12e74d0b9a0257469a13f311'),(35,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTg4MzUzOCwiaWF0IjoxNzM5Mjc4NzM4LCJqdGkiOiI3NjAzNTEyMzFhNjA0NDA2YmQyZDRmMjU2ODE1MGY1YyIsInVzZXJfaWQiOjV9.NnFXUiMh1fW8QzauDF_wXpv9P1LOOCvwGfdPOiazrXo','2025-02-11 12:58:58.446102','2025-02-18 12:58:58.000000',5,'760351231a604406bd2d4f2568150f5c'),(36,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTg4NzYxNSwiaWF0IjoxNzM5MjgyODE1LCJqdGkiOiIyNjFhYWY0MmUxODY0NGYwOGFjMTdmYTc3NTFjZjEyNiIsInVzZXJfaWQiOjV9.RW74hPwXtjlFt4IijOXWlg-8zV-is9FqbsEMX9q_jeQ','2025-02-11 14:06:55.862202','2025-02-18 14:06:55.000000',5,'261aaf42e18644f08ac17fa7751cf126'),(37,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTg4ODE3OSwiaWF0IjoxNzM5MjgzMzc5LCJqdGkiOiIyYzdmZmYwNzc0NjU0OTZhYmQyMDI4NWVmMmVjMDQxZiIsInVzZXJfaWQiOjV9.f3RUUwohH0hgQu3DnRTwZwI3bYNl0t9f7v0wvK8f4TU','2025-02-11 14:16:19.254691','2025-02-18 14:16:19.000000',5,'2c7fff077465496abd20285ef2ec041f'),(38,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTg5MjAwMiwiaWF0IjoxNzM5Mjg3MjAyLCJqdGkiOiJiZWQ1NGZlYjU3Njg0YmZkYmU5ZDZlNjYxMTRiODc1MCIsInVzZXJfaWQiOjV9.s95N_HWGehmhtK1i_Csj8XqNmaN3QmzqnZTywRC-6Jk','2025-02-11 15:20:02.085812','2025-02-18 15:20:02.000000',5,'bed54feb57684bfdbe9d6e66114b8750'),(39,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTg5MzkzNywiaWF0IjoxNzM5Mjg5MTM3LCJqdGkiOiI0ZmJjMjA5NDU1NjU0MGUyOTNkNzMwMzIzMWI3MTc5NSIsInVzZXJfaWQiOjV9.oUeQLwUKuYkACdDNYZTybAIlt8DKwBjxd3WNU04rPIY','2025-02-11 15:52:17.848475','2025-02-18 15:52:17.000000',5,'4fbc2094556540e293d7303231b71795'),(40,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTg5NDYyNSwiaWF0IjoxNzM5Mjg5ODI1LCJqdGkiOiI4N2M5MmZiZDZjMTA0YzI5YjQyNDNhOWI1NWY0NjM4OCIsInVzZXJfaWQiOjV9.lMyn8mH2ANOHqlN7e8xgw1rON-YMfsLUN3RzgWEuHVg','2025-02-11 16:03:45.841464','2025-02-18 16:03:45.000000',5,'87c92fbd6c104c29b4243a9b55f46388'),(41,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTg5NjcyOSwiaWF0IjoxNzM5MjkxOTI5LCJqdGkiOiJmY2VjN2QxY2NkNGI0MjYzYjYzZGQyY2Y3Mzc1ZTE5OSIsInVzZXJfaWQiOjV9.44M8cfIahH5zhQ4tLQU0GS9uKetxPzmyWep9sUtc-l4','2025-02-11 16:38:49.928066','2025-02-18 16:38:49.000000',5,'fcec7d1ccd4b4263b63dd2cf7375e199'),(42,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTkwMDgwMywiaWF0IjoxNzM5Mjk2MDAzLCJqdGkiOiI5ZjRkZTE2MjZmYzA0NThkOTQzYWM3NGI0YmRkZDgxMiIsInVzZXJfaWQiOjV9.1yyqiq9u4iW6TOQqngZQXKUpuEjpEmIrwbmxKKgOYIY','2025-02-11 17:46:43.588910','2025-02-18 17:46:43.000000',5,'9f4de1626fc0458d943ac74b4bddd812'),(43,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTkwNDU4MywiaWF0IjoxNzM5Mjk5NzgzLCJqdGkiOiIwMjM4YmRkMmMyNmQ0YTBlODQ5N2MzMGE3NzNlZDE4MyIsInVzZXJfaWQiOjV9.1pk3rBbjmYsXV6jaAUNzM5wUwKpwn6krir5aVlCT6xY','2025-02-11 18:49:43.231085','2025-02-18 18:49:43.000000',5,'0238bdd2c26d4a0e8497c30a773ed183'),(44,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTkwNDgwNywiaWF0IjoxNzM5MzAwMDA3LCJqdGkiOiJjNzljODVkOWI4YTQ0ZjFjOGEyOWM2MjM2NWI2NDNjYSIsInVzZXJfaWQiOjV9.rsa--F8FsTJ2d1TYy2N_IYSxFhMPkobUvRYMJUVDnsI','2025-02-11 18:53:27.206141','2025-02-18 18:53:27.000000',5,'c79c85d9b8a44f1c8a29c62365b643ca'),(45,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTkwNTczMCwiaWF0IjoxNzM5MzAwOTMwLCJqdGkiOiI3OTRjMjY4ZDA4ZWY0MGExOTdhOWY4ZmNmNzk2ZTRhYiIsInVzZXJfaWQiOjV9.CeUFBm_e9pXLFron_MI1S2i_gfk50dVdhOos_uM1BKk','2025-02-11 19:08:50.347944','2025-02-18 19:08:50.000000',5,'794c268d08ef40a197a9f8fcf796e4ab'),(46,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTkwNTgzMywiaWF0IjoxNzM5MzAxMDMzLCJqdGkiOiJhMDkwMmQyYTU5MGY0OTA0YjI2N2FkMWI2MDZjOTFiOCJ9._ZRTcsHy4dbxiXyunSbKKX_MZ1IebOAJQPC58Yyo76k','2025-02-11 19:10:33.864274','2025-02-18 19:10:33.000000',NULL,'a0902d2a590f4904b267ad1b606c91b8'),(47,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTkwNTg1OCwiaWF0IjoxNzM5MzAxMDU4LCJqdGkiOiI3OGExYTc3ZWZhM2Y0ZjJmYjBkYzdhMjRjMzU4MGI1NyIsInVzZXJfaWQiOjV9.aMlLC_djpfk4yCgupHJeYKgBvJFWknE_vSjCkwMezuU','2025-02-11 19:10:58.559884','2025-02-18 19:10:58.000000',5,'78a1a77efa3f4f2fb0dc7a24c3580b57'),(48,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTkwNTg2MiwiaWF0IjoxNzM5MzAxMDYyLCJqdGkiOiIzMjYyNjM4OTBjYTY0N2NlOWI2YjkxZDIyNTAxNWMzNyJ9.TXb71b3QBDzs8q5pexeJHYNucoASPDbd7nEpr3bgl_I','2025-02-11 19:11:02.051144','2025-02-18 19:11:02.000000',NULL,'326263890ca647ce9b6b91d225015c37'),(49,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTkwNjIzNywiaWF0IjoxNzM5MzAxNDM3LCJqdGkiOiI4YmQzNjFjZmI4OTk0ODY2OGMzNWMwZTUzN2E5MTY3ZSIsInVzZXJfaWQiOjV9.OHjWXkM6I6j4advgRq3Ot8GZv9HJ0jxQn3LUV4kRR_I','2025-02-11 19:17:17.086079','2025-02-18 19:17:17.000000',5,'8bd361cfb89948668c35c0e537a9167e'),(50,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTk2OTU2MiwiaWF0IjoxNzM5MzY0NzYyLCJqdGkiOiIzMzNmMTliZjEzY2U0OGI1YTM1NDNlZTljMDVmMDBmZiIsInVzZXJfaWQiOjV9.QgQap-WFv6onD9ItWknJgOjmDqrJThPy7gvhuzgWcgE','2025-02-12 12:52:42.860812','2025-02-19 12:52:42.000000',5,'333f19bf13ce48b5a3543ee9c05f00ff'),(51,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTk2OTk1NCwiaWF0IjoxNzM5MzY1MTU0LCJqdGkiOiJlMzVhM2M2YmE3YzI0MDI1YTI1NjhhYTE3MjM3ZTVjZSJ9.KZ8wE7TNHCxEijlwsyjCHVQ5MB4SGigpwaNJpZqBVtY','2025-02-12 12:59:14.849266','2025-02-19 12:59:14.000000',NULL,'e35a3c6ba7c24025a2568aa17237e5ce'),(52,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTk3MDA0MywiaWF0IjoxNzM5MzY1MjQzLCJqdGkiOiJhODEwOWQwNTJjMWE0NWQyOThkYTc3OThmOTJkOTJjNCIsInVzZXJfaWQiOjV9.h--tBia2VI3eJQoulC4f-a6Z1c4gkjZA4qusuB6_HO8','2025-02-12 13:00:43.185607','2025-02-19 13:00:43.000000',5,'a8109d052c1a45d298da7798f92d92c4'),(53,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTk3Mzc5NCwiaWF0IjoxNzM5MzY4OTk0LCJqdGkiOiI2ODljZmRhOWRmYmE0YmYxOTM1ZWI1ZmJiMGNlNmQ1YyIsInVzZXJfaWQiOjV9.c1LMRi0pZXQWeWm3YMFsKCoTzWFtwlPq342c93aR-QI','2025-02-12 14:03:14.303737','2025-02-19 14:03:14.000000',5,'689cfda9dfba4bf1935eb5fbb0ce6d5c'),(54,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTk3ODI4MiwiaWF0IjoxNzM5MzczNDgyLCJqdGkiOiIzOTI3M2JiNjdhNzE0Mzc3YjdkZGZjMTgxOWNkNTQzNiIsInVzZXJfaWQiOjV9.bpbdDPkWQ1R8u3LdYScTjB-Dlc2hZ0K-A4JGzJn1PdI','2025-02-12 15:18:02.033605','2025-02-19 15:18:02.000000',5,'39273bb67a714377b7ddfc1819cd5436'),(55,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTk4MjIxNSwiaWF0IjoxNzM5Mzc3NDE1LCJqdGkiOiI5MWU0ZGM5MTNiMDE0ODVkYWMyOGJjOTExMzdmNDkzNCIsInVzZXJfaWQiOjV9.3DBj5-0RukLYcGifgwMe68xVKjTdCQ67ZH9_rE6HVHk','2025-02-12 16:23:35.588933','2025-02-19 16:23:35.000000',5,'91e4dc913b01485dac28bc91137f4934'),(56,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTk4NTkzMCwiaWF0IjoxNzM5MzgxMTMwLCJqdGkiOiI1NTE1ZGJlYWM0MWE0MTcwOTBmZjkzYTM4YTM0NjBkNSIsInVzZXJfaWQiOjV9.I3_KNBQgpdH83NPl9EXPnKKtV5ZFvXTu1-HFD9F-xrk','2025-02-12 17:25:30.212886','2025-02-19 17:25:30.000000',5,'5515dbeac41a417090ff93a38a3460d5'),(57,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTk5MDE0MywiaWF0IjoxNzM5Mzg1MzQzLCJqdGkiOiJiZmM4ZGEwMzlmNTM0ODQ2OGQ5MmQ3N2JjZDE2YWJiMCIsInVzZXJfaWQiOjV9.BckuHX0nidIXC3Y8GYhGaVlDfn0H21sAxLMlISr_RC4','2025-02-12 18:35:43.232106','2025-02-19 18:35:43.000000',5,'bfc8da039f5348468d92d77bcd16abb0'),(58,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDAzMjc3MywiaWF0IjoxNzM5NDI3OTczLCJqdGkiOiJlNDhmY2NmZDk3M2Y0NjYxYWI2YzU0ZGNmNGM2YWMwMyIsInVzZXJfaWQiOjV9.t6C0Ny6Qsua-eojwbYBm2MUHxqB8QTAZ36tiZf7wlQs','2025-02-13 06:26:13.125130','2025-02-20 06:26:13.000000',5,'e48fccfd973f4661ab6c54dcf4c6ac03'),(59,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA0MDUxMSwiaWF0IjoxNzM5NDM1NzExLCJqdGkiOiJhMzg2Yzk3MTVmNGU0ODA3OGM5YTBlZjE3MTY1OTNhOCIsInVzZXJfaWQiOjV9.qqKC4FumokZ2pBOsGgkyexZ40P6CvEPBXuc44ax7XFY','2025-02-13 08:35:11.400375','2025-02-20 08:35:11.000000',5,'a386c9715f4e48078c9a0ef1716593a8'),(60,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA0MTQ3MSwiaWF0IjoxNzM5NDM2NjcxLCJqdGkiOiJlZWEyMzMxN2ZkYjg0ZDU5YWQ0YzVhODdiZjcyYjBhYyJ9.KgSQstaFuRR4Q1UIatvJpMgSlUCLjp_XH77vGjaF-_g','2025-02-13 08:51:11.284135','2025-02-20 08:51:11.000000',NULL,'eea23317fdb84d59ad4c5a87bf72b0ac'),(61,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA0MTQ3NiwiaWF0IjoxNzM5NDM2Njc2LCJqdGkiOiI2MTgxZGY4MWIzODQ0N2Q0OGMyNTczMDY3ZDAxN2M1ZCIsInVzZXJfaWQiOjV9.Zh2FuRODpKnqGp8hsc89vZ03foAlhDqIRMDdSe5WYDg','2025-02-13 08:51:16.821230','2025-02-20 08:51:16.000000',5,'6181df81b38447d48c2573067d017c5d'),(62,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA0NTMzNywiaWF0IjoxNzM5NDQwNTM3LCJqdGkiOiI1OTc0YWFmNTU1YmE0NWUwOGQ3YzMwM2EwMzNmNjhkYyIsInVzZXJfaWQiOjV9.e51osHPtJ9MfhZP8GEebDxfIBE5lb8kHnhVvpPxQH38','2025-02-13 09:55:37.890800','2025-02-20 09:55:37.000000',5,'5974aaf555ba45e08d7c303a033f68dc'),(63,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA1Mzk3NCwiaWF0IjoxNzM5NDQ5MTc0LCJqdGkiOiJiNmZmYmJkZGUyZTE0NTkzOWUxZTRhMTFmMWQ3ZTk4NiIsInVzZXJfaWQiOjV9.O_f_Eazoa5UANmVSixLGy6wi9Z6Hpe1L00LIh0AG_NQ','2025-02-13 12:19:34.038896','2025-02-20 12:19:34.000000',5,'b6ffbbdde2e145939e1e4a11f1d7e986'),(64,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA1Nzg2NiwiaWF0IjoxNzM5NDUzMDY2LCJqdGkiOiIyOWU5YzQ2MTUyNzM0MDkyODExMjMyZDg0NWVjYmYyMiIsInVzZXJfaWQiOjV9.jJB4krR-GbQ_VMW6USQ4QviHEAyTjBItVu_7NQ8hTiw','2025-02-13 13:24:26.696267','2025-02-20 13:24:26.000000',5,'29e9c46152734092811232d845ecbf22'),(65,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA1ODk4NSwiaWF0IjoxNzM5NDU0MTg1LCJqdGkiOiJjZjFhMGZmYTg3NDA0NWYwYmY5OWY3MjVjMzRiMGJmNCJ9.pZp2qIY_7_mNBd425G5oEOCjLJxin9ij2CBfw0bX6B4','2025-02-13 13:43:05.176615','2025-02-20 13:43:05.000000',NULL,'cf1a0ffa874045f0bf99f725c34b0bf4'),(66,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA1ODk4NSwiaWF0IjoxNzM5NDU0MTg1LCJqdGkiOiIwY2RkYWUzNDlmNjk0ODkzYmI4ZjAyYjk2ZGY4NmNjZSJ9.hLsFgTFMiKbEzni0PbPcdLKvEnMleU0tgsoSb4duPIY','2025-02-13 13:43:05.177615','2025-02-20 13:43:05.000000',NULL,'0cddae349f694893bb8f02b96df86cce'),(67,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA1ODk5MywiaWF0IjoxNzM5NDU0MTkzLCJqdGkiOiI5MzkxNDI5Mjc3MjE0MWRmYWQyMWY1MDNiZTkwNGE5YiIsInVzZXJfaWQiOjV9.xt01xQ9vMO3PwqgTgkAqQ4D4vFYh3mK65BiDZnnU9B4','2025-02-13 13:43:13.621025','2025-02-20 13:43:13.000000',5,'93914292772141dfad21f503be904a9b'),(68,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA1OTUzOCwiaWF0IjoxNzM5NDU0NzM4LCJqdGkiOiI0MzBjMmQ0YmQ3MzY0MTEyYmNlY2U1MmVkN2QyOWZiMSJ9.JKZhGfo7yTw6ZBVOmaZw0Eqnx8XmJiSJs5HSSKryBzM','2025-02-13 13:52:18.223367','2025-02-20 13:52:18.000000',NULL,'430c2d4bd7364112bcece52ed7d29fb1'),(69,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA1OTU0MiwiaWF0IjoxNzM5NDU0NzQyLCJqdGkiOiJkMzUxYzAzMjUyNGI0NWFlOGE0ODAyYTJmOTUxODY1ZCIsInVzZXJfaWQiOjV9.ZeHkCiIO4wlMql0ojXwq3s83173j9bJgbbmD7Fy2yi4','2025-02-13 13:52:22.103423','2025-02-20 13:52:22.000000',5,'d351c032524b45ae8a4802a2f951865d'),(70,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA1OTk3NSwiaWF0IjoxNzM5NDU1MTc1LCJqdGkiOiI5ODk1NmU3MTI3ZmQ0ZTY2YWI0YzQxMDNkYTMwZGUxZSJ9.Dlyz6O_q8jWZhxxel66imkNDrxOE--WfbmRmvnCkg-E','2025-02-13 13:59:35.105451','2025-02-20 13:59:35.000000',NULL,'98956e7127fd4e66ab4c4103da30de1e'),(71,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA1OTk3NywiaWF0IjoxNzM5NDU1MTc3LCJqdGkiOiJjNmIxYjI0YTczOGE0ZDRlOGE2YzNmZWYyMGNkZGMyMSIsInVzZXJfaWQiOjV9.EQli1520B5Ow8hGIfC722SV4gap5O8-8ddIMddydADI','2025-02-13 13:59:37.190941','2025-02-20 13:59:37.000000',5,'c6b1b24a738a4d4e8a6c3fef20cddc21'),(72,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA2Mzg3MiwiaWF0IjoxNzM5NDU5MDcyLCJqdGkiOiIyMmZmOTYzMDI3YmI0ZWJkYTZlZTYxYjNkZWVkMjZmMCIsInVzZXJfaWQiOjV9.-1ULNb4NwKsImHYsdi2YaB0kuNv_uds2I-yf2cODW8c','2025-02-13 15:04:32.989267','2025-02-20 15:04:32.000000',5,'22ff963027bb4ebda6ee61b3deed26f0'),(73,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA2NzUyMCwiaWF0IjoxNzM5NDYyNzIwLCJqdGkiOiI2YTY1MTM3ZTJmZGI0ZDY2YmQzMjdlMjcxYTMwZjU4NyIsInVzZXJfaWQiOjV9.xQR37OKClESiUH4_TBA8aHaba8kHR27_esWGZ58JvgA','2025-02-13 16:05:20.384694','2025-02-20 16:05:20.000000',5,'6a65137e2fdb4d66bd327e271a30f587'),(74,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDA3MTg2NCwiaWF0IjoxNzM5NDY3MDY0LCJqdGkiOiIwZmEwOGI1YzQwZTQ0ZGU2YWI4NTA3OTY1NDM2ODI4NCIsInVzZXJfaWQiOjV9.P1o9XAeU0_rGp6SquIFM78RG1vGBNOVP6CmaVA4wHIA','2025-02-13 17:17:44.066144','2025-02-20 17:17:44.000000',5,'0fa08b5c40e44de6ab85079654368284'),(75,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDEyNzQ5MCwiaWF0IjoxNzM5NTIyNjkwLCJqdGkiOiI2NGJlY2YzODI5OGU0N2Q2OGNhMjA4NDAyMDk5OTJiNyIsInVzZXJfaWQiOjV9.2nI1UG0HMs1Kr90EHzcVMIdpNnWMHF3scde9TJy7eJ8','2025-02-14 08:44:50.463154','2025-02-21 08:44:50.000000',5,'64becf38298e47d68ca20840209992b7'),(76,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDMxNTM3OSwiaWF0IjoxNzM5NzEwNTc5LCJqdGkiOiIyYjQ5OTRhOGQwOTU0ZWQzOGEzYjQzNzI4ZmEwZjEwZCIsInVzZXJfaWQiOjV9.cpZC74dZrL-Q0tWOJsyXawAHrH9MORuwMZuwm-3Bwh4','2025-02-16 12:56:19.800640','2025-02-23 12:56:19.000000',5,'2b4994a8d0954ed38a3b43728fa0f10d'),(77,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDMxODk5OSwiaWF0IjoxNzM5NzE0MTk5LCJqdGkiOiI5OTQxYjNiNTkzMTQ0MDc3ODY1OTFiMTcyNDZhZWEyMiIsInVzZXJfaWQiOjV9.FBR0XoJdxi8RP4ailD8qLybqNnnTiOKElbUQ-A8Xv5A','2025-02-16 13:56:39.475767','2025-02-23 13:56:39.000000',5,'9941b3b59314407786591b17246aea22'),(78,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDMyMjcwMCwiaWF0IjoxNzM5NzE3OTAwLCJqdGkiOiI5NDlmOTU1ZGY1N2U0NzE1OTNhNTE2OTliZTdiMmVkYiIsInVzZXJfaWQiOjV9.49mb-AtXXJoV4m8up0WODWMl90tnEP-ssjy079ajopQ','2025-02-16 14:58:20.270283','2025-02-23 14:58:20.000000',5,'949f955df57e471593a51699be7b2edb'),(79,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDMyNjg4NCwiaWF0IjoxNzM5NzIyMDg0LCJqdGkiOiIzYjM0NGFhNjA2YTE0OTA1ODM5ZTI5OGE1ZTZmOGFlNSIsInVzZXJfaWQiOjV9.WxWZK_N8DRyX-wGoXX5wBeiyKROaS9Jm5YdlUIeWwyw','2025-02-16 16:08:04.852203','2025-02-23 16:08:04.000000',5,'3b344aa606a14905839e298a5e6f8ae5'),(80,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDMzMjAxMiwiaWF0IjoxNzM5NzI3MjEyLCJqdGkiOiJjZTJjYzU4YzdlMTM0OTg4ODkzZGYzNDA0ZjNhMjRkNCIsInVzZXJfaWQiOjV9.Y3B_PAZTarr0SmjMiKNm_N6re7NDzQyCFzWLT9O30Po','2025-02-16 17:33:32.138088','2025-02-23 17:33:32.000000',5,'ce2cc58c7e134988893df3404f3a24d4'),(81,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDMzNTY0NSwiaWF0IjoxNzM5NzMwODQ1LCJqdGkiOiJlZDY5ZjJkNzBiMWY0MDM1OGY0M2MzZTU0ZTIwOGIzMCIsInVzZXJfaWQiOjV9.AvZpF5VlY4934YiI4yG4tq9cygrggcmAv3maX-aGRdE','2025-02-16 18:34:05.297114','2025-02-23 18:34:05.000000',5,'ed69f2d70b1f40358f43c3e54e208b30'),(82,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDMzOTQ0NiwiaWF0IjoxNzM5NzM0NjQ2LCJqdGkiOiJmZDIxOGQyNjBkNGY0ZTg5OTRhMWRlMDlhZjExMmYzNCIsInVzZXJfaWQiOjV9.T4dhaETTLyHBaOX7IH8xOMPQiBHSZW-pfpwRZ48BNjo','2025-02-16 19:37:26.015820','2025-02-23 19:37:26.000000',5,'fd218d260d4f4e8994a1de09af112f34'),(83,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDM2MTkzMiwiaWF0IjoxNzM5NzU3MTMyLCJqdGkiOiIzODg0ZDMzOWIxMzk0NzI5YTk5ODkwMzJmMGZkOGExOCIsInVzZXJfaWQiOjV9.uEK8-KBVXQ34EAFkuvZj9JY5WQzwj9T_Ocnvu3-ITnE','2025-02-17 01:52:12.499283','2025-02-24 01:52:12.000000',5,'3884d339b1394729a9989032f0fd8a18'),(84,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDM2NjAyNSwiaWF0IjoxNzM5NzYxMjI1LCJqdGkiOiJkY2NjYzA3ODZlOTU0NzI0ODFjZDg3MTQxNjIwMDEzNiIsInVzZXJfaWQiOjV9.lvmer5bkPMYW7VW7L2e3LTGCW8Ap7qiq4zsotnv9t6E','2025-02-17 03:00:25.744683','2025-02-24 03:00:25.000000',5,'dcccc0786e95472481cd871416200136'),(85,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDM3MDg1NiwiaWF0IjoxNzM5NzY2MDU2LCJqdGkiOiI2MDRkMTE4YzUxYmY0NmVhOGFlNjc4M2NmMjE5ZjFhZiIsInVzZXJfaWQiOjV9.B39Qi5Kk1iydaAfzFgs8E7p07kJHgzRbhh0DP-fvpXc','2025-02-17 04:20:56.937215','2025-02-24 04:20:56.000000',5,'604d118c51bf46ea8ae6783cf219f1af'),(86,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDQ2MTQ3NSwiaWF0IjoxNzM5ODU2Njc1LCJqdGkiOiJjZWU3ZmM0ZDcwYzk0OTQyYWZmN2NlNGZkZjhjOWNhMyIsInVzZXJfaWQiOjV9._jBYRI1WbgRcWMP9G1yw_6rklkjOtmbGnrE9Ip4ZmRs','2025-02-18 05:31:15.791943','2025-02-25 05:31:15.000000',5,'cee7fc4d70c94942aff7ce4fdf8c9ca3'),(87,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDQ2NTA4MywiaWF0IjoxNzM5ODYwMjgzLCJqdGkiOiI1MzU5OGFjNzk2NGE0YjU3YWEzMjljNDBlNTg1NGMwZiIsInVzZXJfaWQiOjV9.3IdAeIRILVDtyW9Us90r9tC7Pi2lXe-9n3Bwcq4Rfdw','2025-02-18 06:31:23.940051','2025-02-25 06:31:23.000000',5,'53598ac7964a4b57aa329c40e5854c0f'),(88,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDQ2ODc2MSwiaWF0IjoxNzM5ODYzOTYxLCJqdGkiOiI4ZmY0ODM0NWRhNzg0ZDk4ODdjMWVkNmZiN2JkNjU1NCIsInVzZXJfaWQiOjV9.DQ5kXJ1J7s_Kx0ogCUVY-NHO86sczClU7ldOju8i8r8','2025-02-18 07:32:41.520315','2025-02-25 07:32:41.000000',5,'8ff48345da784d9887c1ed6fb7bd6554'),(89,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDQ5MzAzOSwiaWF0IjoxNzM5ODg4MjM5LCJqdGkiOiJmNjUxYmEzY2NmZDQ0MzFiODk3OWU4OGYwOWI3OWQzMCIsInVzZXJfaWQiOjV9.3lf28ubMU6q3uEwYUJaOc2h12O5rhvt76crCCjMxles','2025-02-18 14:17:19.440317','2025-02-25 14:17:19.000000',5,'f651ba3ccfd4431b8979e88f09b79d30'),(90,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDQ5Njc4NywiaWF0IjoxNzM5ODkxOTg3LCJqdGkiOiI3OWZlOTBiODk1NDU0NTA4YWU5ODFjNzM1MzQwN2ZjZSIsInVzZXJfaWQiOjV9.RTjTQx-hEnoZNBs7bv3uGsofQGKJf_arvO5nnYJCNQo','2025-02-18 15:19:47.410703','2025-02-25 15:19:47.000000',5,'79fe90b895454508ae981c7353407fce'),(91,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDUwMDUzMywiaWF0IjoxNzM5ODk1NzMzLCJqdGkiOiJhOGU1ZmI1MjJjZmE0YzliODI0ZTg2NDAxODFhM2M5NCIsInVzZXJfaWQiOjV9.zDoxSZqQUz-21pdvX879CaJiylX5VPFgKsSppXZi7bA','2025-02-18 16:22:13.420277','2025-02-25 16:22:13.000000',5,'a8e5fb522cfa4c9b824e8640181a3c94'),(92,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDUwNDE0MCwiaWF0IjoxNzM5ODk5MzQwLCJqdGkiOiIyNmE5MWY1YzliZTA0MGZkYjRhZDQ1YWEyOGVhMTc4NyIsInVzZXJfaWQiOjV9.2-k015G39Tp42RtUl140krAvmAJDg6Iy1q-E1Rp7QkY','2025-02-18 17:22:20.544070','2025-02-25 17:22:20.000000',5,'26a91f5c9be040fdb4ad45aa28ea1787'),(93,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDUwNzk5OCwiaWF0IjoxNzM5OTAzMTk4LCJqdGkiOiJmZWNkYzExN2ZlYzk0YWU1OGI0ZmZiZWM2MmU0YmM1ZiIsInVzZXJfaWQiOjV9.W1X9bxgU3XbU0DqRpnhEO7pI6KO5FYXzASn9Hl56-Yk','2025-02-18 18:26:38.329245','2025-02-25 18:26:38.000000',5,'fecdc117fec94ae58b4ffbec62e4bc5f'),(94,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDUxMTc4MywiaWF0IjoxNzM5OTA2OTgzLCJqdGkiOiI0Y2UyODA0OWVlMzc0Zjk0YWNhYTIyZDdiN2NlMzQzYiIsInVzZXJfaWQiOjV9.lcGIO33LaRSrybVTava0sbbp2znUqVl_pbQl_39PtAE','2025-02-18 19:29:43.938211','2025-02-25 19:29:43.000000',5,'4ce28049ee374f94acaa22d7b7ce343b'),(95,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDUzMTk3MCwiaWF0IjoxNzM5OTI3MTcwLCJqdGkiOiJkMDQ0OTVlNGU3MmQ0YzZiOWI1ZmE1NDZkMDMwZWI5ZiIsInVzZXJfaWQiOjV9.djJUlLeQN8ihfV3uxHhWHPDWA4ik9LRo2FEgkxbujkY','2025-02-19 01:06:10.226390','2025-02-26 01:06:10.000000',5,'d04495e4e72d4c6b9b5fa546d030eb9f'),(96,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDU3NDg3NSwiaWF0IjoxNzM5OTcwMDc1LCJqdGkiOiJlOGNhY2EyMmIxMjM0Y2VjYmM4ZmJlN2I1ZDQ1MjE3YSIsInVzZXJfaWQiOjV9.GVQZ7g9IeDEpRxJiBGrRUfnL_QEjSbLv1jdhbZCzwew','2025-02-19 13:01:15.763260','2025-02-26 13:01:15.000000',5,'e8caca22b1234cecbc8fbe7b5d45217a'),(97,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDU3ODc3OSwiaWF0IjoxNzM5OTczOTc5LCJqdGkiOiJjN2JmMWQ4ODY1ZmQ0OWZjOTVjN2Y4MWYwYTUzNDM3YSIsInVzZXJfaWQiOjV9.EwCfQDMS24WQrIvENjzc0zsDfmzP-EVt0qTj45ZOp90','2025-02-19 14:06:19.119435','2025-02-26 14:06:19.000000',5,'c7bf1d8865fd49fc95c7f81f0a53437a'),(98,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDU4MjQxMSwiaWF0IjoxNzM5OTc3NjExLCJqdGkiOiIyMjM5MTJlZmM3ZmQ0MGZhODdhOWNhNGFlM2Y2N2I0NSIsInVzZXJfaWQiOjV9.7fKmn6MwXMZ8DR3u9HD_HIcnO7Ih2bl8RYtsvGz7bHc','2025-02-19 15:06:51.586445','2025-02-26 15:06:51.000000',5,'223912efc7fd40fa87a9ca4ae3f67b45'),(99,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDU4NzQyOCwiaWF0IjoxNzM5OTgyNjI4LCJqdGkiOiI3YzAxZmNlYTk0ZGQ0ZmRlODlhYzI5ZGNjOGYyYmEzZCIsInVzZXJfaWQiOjV9.Ws7n-yta4U5kxEM6516CxINjZRLaiCxva3WkLoJONho','2025-02-19 16:30:28.240245','2025-02-26 16:30:28.000000',5,'7c01fcea94dd4fde89ac29dcc8f2ba3d'),(100,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDU5MTMyMSwiaWF0IjoxNzM5OTg2NTIxLCJqdGkiOiIxMjI2YjliZGFlNGE0MjQ3OTdjY2ZjYmI3ZjM3N2FiNCIsInVzZXJfaWQiOjV9.rABbYZxLwUFgBOCYF-VfegL7twVCIcNhWG9c19AGB9w','2025-02-19 17:35:21.327991','2025-02-26 17:35:21.000000',5,'1226b9bdae4a424797ccfcbb7f377ab4'),(101,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDU5NjM1NywiaWF0IjoxNzM5OTkxNTU3LCJqdGkiOiI4ZjY1YzhjYzFkMGQ0NTU4ODk4YmYwYzM0ZmNhZTU0MCIsInVzZXJfaWQiOjV9.oLHg0_U_lfJJU7V3WcGo2Y9elk06DodWcR_kcmYfk8A','2025-02-19 18:59:17.313707','2025-02-26 18:59:17.000000',5,'8f65c8cc1d0d4558898bf0c34fcae540'),(102,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDY0NjE2NSwiaWF0IjoxNzQwMDQxMzY1LCJqdGkiOiJhZGRjMTNhMTBiMTE0ZGU4ODdiN2U5OGRhOWY2MzZkMSIsInVzZXJfaWQiOjV9.BxL6jS6Xy_4Y5_kAdU1Mj58OkxbeBIAV8m3PVt8HaQU','2025-02-20 08:49:25.683802','2025-02-27 08:49:25.000000',5,'addc13a10b114de887b7e98da9f636d1'),(103,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDY1NzcxMiwiaWF0IjoxNzQwMDUyOTEyLCJqdGkiOiI2NzNmYzI0ZWZiZjA0ODZjOWJhMzJkN2NjNTYwZjk2ZSIsInVzZXJfaWQiOjV9.K_Y5ODT4vgH07BuRT1r98qMQ_Ygblkh07LnvPp2-nbM','2025-02-20 12:01:52.298483','2025-02-27 12:01:52.000000',5,'673fc24efbf0486c9ba32d7cc560f96e'),(104,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDY2MjI0NiwiaWF0IjoxNzQwMDU3NDQ2LCJqdGkiOiJjMTU5NDQxYTEzMmY0ODg1YjdkN2M5M2UwNjcyMjVjOSIsInVzZXJfaWQiOjV9.392QLLHpKdGWbYkgpec3iSyT7LHUfkDNYhObYNPA5dI','2025-02-20 13:17:26.527218','2025-02-27 13:17:26.000000',5,'c159441a132f4885b7d7c93e067225c9'),(105,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDY2NTg3OSwiaWF0IjoxNzQwMDYxMDc5LCJqdGkiOiIyYTBmZDZmYTAxYWY0YmE3OGMxY2I4MDg1MTUyY2QwZSIsInVzZXJfaWQiOjV9.SLYHtIZV0zK9eIfGbyUUwgE-2xOlxZ9c14Bm8kNzxHI','2025-02-20 14:17:59.992064','2025-02-27 14:17:59.000000',5,'2a0fd6fa01af4ba78c1cb8085152cd0e'),(106,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDY3MDM0OSwiaWF0IjoxNzQwMDY1NTQ5LCJqdGkiOiIzMDlkZGI1NDk0Y2I0OTJmYTE5N2NlYjI3ZTdjNWFlNiIsInVzZXJfaWQiOjV9.NbOS39vI0uN1IdfYppi1e7eOm34lp98yQI56goLtFr0','2025-02-20 15:32:29.104285','2025-02-27 15:32:29.000000',5,'309ddb5494cb492fa197ceb27e7c5ae6'),(107,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDY3NDAwMCwiaWF0IjoxNzQwMDY5MjAwLCJqdGkiOiI3Y2Y3ZWRjZDQ5NGY0NTJiYjgxZGRkOTM3ZjMzMTBjOCIsInVzZXJfaWQiOjV9.J_oLYb98j7JR0Lb9kDq5ixi2PubmK-OSU2fE8FqQCoQ','2025-02-20 16:33:20.774934','2025-02-27 16:33:20.000000',5,'7cf7edcd494f452bb81ddd937f3310c8'),(108,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDY3Nzg1NiwiaWF0IjoxNzQwMDczMDU2LCJqdGkiOiJmMjA2NWFlMGVjY2I0Mzg1YTc3YTllMTA0NWVjMDE3YSIsInVzZXJfaWQiOjV9.pdd3vFpHKn4T-43746bO5ZTL7eN82RmfY0ovgV58QjQ','2025-02-20 17:37:36.218728','2025-02-27 17:37:36.000000',5,'f2065ae0eccb4385a77a9e1045ec017a'),(109,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDY4MTQ5OCwiaWF0IjoxNzQwMDc2Njk4LCJqdGkiOiIyMmI1NjEyZDQwYmM0Y2I5YmI4MDI1ZDQ1Y2QyNDBjOSIsInVzZXJfaWQiOjV9.HqxjDRD0CUqn1K-M-Un_zSqjpW5kOo9tvJi4F0wCfks','2025-02-20 18:38:18.486856','2025-02-27 18:38:18.000000',5,'22b5612d40bc4cb9bb8025d45cd240c9'),(110,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDY4NTYwMywiaWF0IjoxNzQwMDgwODAzLCJqdGkiOiJhOTFjNzljZGZmZjQ0NTcwYjE1YzFjOGU2ZTkzMzY3MSIsInVzZXJfaWQiOjV9.juGU2riWerIOSb0a19zauAr_i7wsAe362go_KTSx9Ic','2025-02-20 19:46:43.268644','2025-02-27 19:46:43.000000',5,'a91c79cdfff44570b15c1c8e6e933671'),(111,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDc0NzIwMywiaWF0IjoxNzQwMTQyNDAzLCJqdGkiOiJhZjRiNDdiMjQ5NDU0Nzk2YjJiNmJhN2IyMDFiYmExYiIsInVzZXJfaWQiOjV9.MFO8pglobFt7DM9bOiNXCLulOd9WgXa6Pr58ZLJkP_s','2025-02-21 12:53:23.039793','2025-02-28 12:53:23.000000',5,'af4b47b249454796b2b6ba7b201bba1b'),(112,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDc1MDg4OSwiaWF0IjoxNzQwMTQ2MDg5LCJqdGkiOiI0ZjNkNjQ3NzliMmY0YmU4YjY5YTA1YmZiOWE5NzJiYiIsInVzZXJfaWQiOjV9.hqA-Q7CHSXf-qlhEN9_eeRgFSlDFaXW223c6iSEzhjw','2025-02-21 13:54:49.971213','2025-02-28 13:54:49.000000',5,'4f3d64779b2f4be8b69a05bfb9a972bb'),(113,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDc1NDU4NSwiaWF0IjoxNzQwMTQ5Nzg1LCJqdGkiOiIyZWFjYjgxMTIyZjc0MTdkYWE4YTdhMDgxYzg3ZmMzYSIsInVzZXJfaWQiOjV9.2Cqn5jDng_OsP0X4aTON-QnQ9h1YMuGuYD4nX_gWxUs','2025-02-21 14:56:25.505439','2025-02-28 14:56:25.000000',5,'2eacb81122f7417daa8a7a081c87fc3a'),(114,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDc1ODIzMiwiaWF0IjoxNzQwMTUzNDMyLCJqdGkiOiJhMzA0MDgxYTA2MmU0MWZhOTJlZTgyNTQ3NTBkNWIwMCIsInVzZXJfaWQiOjV9.CZ-JiMgQuE38cbIREJB6snFIOCmU8Tqbsck2j65EOn0','2025-02-21 15:57:12.523735','2025-02-28 15:57:12.000000',5,'a304081a062e41fa92ee8254750d5b00'),(115,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDc2MTg0MCwiaWF0IjoxNzQwMTU3MDQwLCJqdGkiOiI4ZmQ5NWRkMmUxMWM0YTZiODE3NjljZGI3MzdiMTE2NyIsInVzZXJfaWQiOjV9.PE7czq-5b-OC2fVBKSm1gebjgcE1kQrJG7ikx_PJz-c','2025-02-21 16:57:20.895496','2025-02-28 16:57:20.000000',5,'8fd95dd2e11c4a6b81769cdb737b1167'),(116,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDc2NTY4MywiaWF0IjoxNzQwMTYwODgzLCJqdGkiOiJiOTRkOGFkYWZhMmU0YTJjODBhNWZiZDgyNWMyZjk0YSIsInVzZXJfaWQiOjV9.5O10De_aXrzCytg6A_DCWPkJg9jfBx2bccTkl6gJwzM','2025-02-21 18:01:23.328696','2025-02-28 18:01:23.000000',5,'b94d8adafa2e4a2c80a5fbd825c2f94a'),(117,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAwMzI2OSwiaWF0IjoxNzQwMzk4NDY5LCJqdGkiOiJmMWMwMmUzMmQ5OWU0ZGFlOTIzMThhODJlNjNlYjAyNiIsInVzZXJfaWQiOjV9.QR3iicLlykuKh7vGbFhPuE4AP44PtLldLl7_xG7pRSs','2025-02-24 12:01:09.287444','2025-03-03 12:01:09.000000',5,'f1c02e32d99e4dae92318a82e63eb026'),(118,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAwNjg4OSwiaWF0IjoxNzQwNDAyMDg5LCJqdGkiOiIwYzNhNTk4YzMzZDU0MGE1OGM1NmM4OWM0ZTM1YTcxOCIsInVzZXJfaWQiOjV9.fnGN8ljxngx3NxQAXvSGxGVhF_1E9EEaRc-IYYEVRkY','2025-02-24 13:01:29.611432','2025-03-03 13:01:29.000000',5,'0c3a598c33d540a58c56c89c4e35a718'),(119,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAxMDk0NCwiaWF0IjoxNzQwNDA2MTQ0LCJqdGkiOiIxZWUwNjA1MDZlNTc0NDE4ODhlMDg3YzhjZDcxMzhkZSIsInVzZXJfaWQiOjV9.1-bFwaDZIiicLTYmLKcBU9Q12NQvY0Y6DMK24unKEiY','2025-02-24 14:09:04.635572','2025-03-03 14:09:04.000000',5,'1ee060506e57441888e087c8cd7138de'),(120,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAyMDEzNCwiaWF0IjoxNzQwNDE1MzM0LCJqdGkiOiI3MGNlOWE5MWE1OGQ0MmNhODVmNmM5NTVhNzZlYjE0MyIsInVzZXJfaWQiOjV9.ibxWZYsDAKA93eDTS9hUL5jVKbHhIvdMMCxwRnk-2_Q','2025-02-24 16:42:14.037640','2025-03-03 16:42:14.000000',5,'70ce9a91a58d42ca85f6c955a76eb143'),(121,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAyMzk4NSwiaWF0IjoxNzQwNDE5MTg1LCJqdGkiOiJkY2FhNTEzMmMyODM0NzA0YTc3MzM1ZTQzNzJiOGM4NCIsInVzZXJfaWQiOjV9.R2ih8bhPVQ7yQxQCKfOY0YkdlG_lshWgj2RvUEYmj9U','2025-02-24 17:46:25.019182','2025-03-03 17:46:25.000000',5,'dcaa5132c2834704a77335e4372b8c84'),(122,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAyNDc2NiwiaWF0IjoxNzQwNDE5OTY2LCJqdGkiOiJhYzFlNGYyMmExZDY0OWIzYTY1MzMwYzE1M2NmZGE4ZCIsInVzZXJfaWQiOjV9.di_i1OhF0OxAr2Owh2MitZ-n3p0XceaKQ4CoeKaNa0M','2025-02-24 17:59:26.107609','2025-03-03 17:59:26.000000',5,'ac1e4f22a1d649b3a65330c153cfda8d'),(123,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAyNDgzMCwiaWF0IjoxNzQwNDIwMDMwLCJqdGkiOiI1OWFkMzY0NGUzNWQ0MWUxYTlkMTQwYWU3YWMzOWQxYyIsInVzZXJfaWQiOjV9.XC5SOqp2G3X18mX5pw8kbUUyW6cRgQUFDmVrM8pU-SU','2025-02-24 18:00:30.835612','2025-03-03 18:00:30.000000',5,'59ad3644e35d41e1a9d140ae7ac39d1c'),(124,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAyNDg4MSwiaWF0IjoxNzQwNDIwMDgxLCJqdGkiOiJlMmJhM2IwYjhhY2E0NmY5OWFlZWE1NDI4NTYzZGU3YyIsInVzZXJfaWQiOjV9.GDa_AccA7EQgKepZ3LAnOxRjb9n09RIGuuBIOxfSZQE','2025-02-24 18:01:21.943616','2025-03-03 18:01:21.000000',5,'e2ba3b0b8aca46f99aeea5428563de7c'),(125,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAyNTA0MywiaWF0IjoxNzQwNDIwMjQzLCJqdGkiOiJmZTY4ODkwMjE0NTk0Nzg5ODZkMjIyNjNhNDVmN2RhOCIsInVzZXJfaWQiOjV9.qSs3kV-In1_kFi1yMsxYxnis1XvhxwfcKhm9ODCOR_E','2025-02-24 18:04:03.600177','2025-03-03 18:04:03.000000',5,'fe6889021459478986d22263a45f7da8'),(126,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAyNTE1MSwiaWF0IjoxNzQwNDIwMzUxLCJqdGkiOiJkMGY4Y2E2NmIzZDg0ODgyYTkyOWVjNzU1YmFkMmU2OCIsInVzZXJfaWQiOjV9.brjRObalMZJNkqv-9mIQrYTBMpK_fwR8ugN2jkha6v8','2025-02-24 18:05:51.526968','2025-03-03 18:05:51.000000',5,'d0f8ca66b3d84882a929ec755bad2e68'),(127,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAyNTIxOCwiaWF0IjoxNzQwNDIwNDE4LCJqdGkiOiI2NjQ0Zjk1MzhjYWE0OTdhOThhYzc3Yjk5YWQ3MmIyOCIsInVzZXJfaWQiOjV9.uv_ipo9ko373MkBmhihrmwZ2KRPYJYbV66GCKQkCmss','2025-02-24 18:06:58.792187','2025-03-03 18:06:58.000000',5,'6644f9538caa497a98ac77b99ad72b28'),(128,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAyNTMyOSwiaWF0IjoxNzQwNDIwNTI5LCJqdGkiOiIyYWI4NDg2Njc0YTU0MDc5ODIwN2FkOGUzMTY1NDE4YSIsInVzZXJfaWQiOjV9.XdnxUyLagHhmv2LiRe0qsm_bVKVUkgFnTInnRN451bE','2025-02-24 18:08:49.351614','2025-03-03 18:08:49.000000',5,'2ab8486674a540798207ad8e3165418a'),(129,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAyNTUxMSwiaWF0IjoxNzQwNDIwNzExLCJqdGkiOiI1Yjk5MTQ5OThhYWE0OWQxOWQ5ZDZhNjQxMmE0ZjJiOCIsInVzZXJfaWQiOjV9.-lTXEKlLhyHu9RCUkM85az01W85ycbuPVtUGSCjKdy0','2025-02-24 18:11:51.958100','2025-03-03 18:11:51.000000',5,'5b9914998aaa49d19d9d6a6412a4f2b8'),(130,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAyNTUzMywiaWF0IjoxNzQwNDIwNzMzLCJqdGkiOiIyMDMzZTE5ZDdlMDE0MDViYjRiMGM4NDU3NDE3YTNmNCIsInVzZXJfaWQiOjV9.WuQcv3POFWJTkpV-gJjNMH-i3dzb2R_9EDjXCuT5MIo','2025-02-24 18:12:13.296836','2025-03-03 18:12:13.000000',5,'2033e19d7e01405bb4b0c8457417a3f4'),(131,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAyNzkwOSwiaWF0IjoxNzQwNDIzMTA5LCJqdGkiOiI1OTg3ODJiZmYwODQ0MzVhYjhmM2M3ZDRkZjAwODgyNSIsInVzZXJfaWQiOjV9.-U4ONmgY-FOXwg29NxKk9CI9-hGbY1WAYVRSupgWIis','2025-02-24 18:51:49.850474','2025-03-03 18:51:49.000000',5,'598782bff084435ab8f3c7d4df008825'),(132,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTAyODk0NSwiaWF0IjoxNzQwNDI0MTQ1LCJqdGkiOiI0OWVkZTlhZmU3YzY0NmJjYWY0ZmRmYTY2Zjk1ODBlNSIsInVzZXJfaWQiOjV9.6Z08oG03nXS7t9kAa8UJ6nOQrQQr-6JZlkqM9Z97OQE','2025-02-24 19:09:05.444460','2025-03-03 19:09:05.000000',5,'49ede9afe7c646bcaf4fdfa66f9580e5'),(133,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTA0ODM3MCwiaWF0IjoxNzQwNDQzNTcwLCJqdGkiOiIwYjI0ZWUxODRkNmY0NjIyYjFlNTE1ZTJmYjYwZTFmMyIsInVzZXJfaWQiOjV9.OoOfJEoJ5upQtrIPT9dMF59Bhtj7UWjnyAVu1gPPtx8','2025-02-25 00:32:50.745780','2025-03-04 00:32:50.000000',5,'0b24ee184d6f4622b1e515e2fb60e1f3'),(134,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTA2Njc1OSwiaWF0IjoxNzQwNDYxOTU5LCJqdGkiOiI0MWQ0YjA1NGMzNDI0MjdhYmU3MmU4OWY1ZmNjNGJlOSIsInVzZXJfaWQiOjV9.DPZusjzmf2Ly4FeLGvCbvB-w6dFK0T6oifW17ZIqBLo','2025-02-25 05:39:19.716456','2025-03-04 05:39:19.000000',5,'41d4b054c342427abe72e89f5fcc4be9'),(135,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTA4MTM4NCwiaWF0IjoxNzQwNDc2NTg0LCJqdGkiOiI1NWQxMTJhZTI0Mjc0YTRkOGMzOTRhMzQ2YWEyZGFiNiIsInVzZXJfaWQiOjV9.cnqYctNzfNY_zanCp0Lqk1gI-vHVg7fI2l-tf2zZ1x0','2025-02-25 09:43:04.975479','2025-03-04 09:43:04.000000',5,'55d112ae24274a4d8c394a346aa2dab6'),(136,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTA5MTc4MCwiaWF0IjoxNzQwNDg2OTgwLCJqdGkiOiIyOGM4Njg3MzA4ZjE0Y2NlYjkwYWU4OGEwMDNiMDUwOCIsInVzZXJfaWQiOjV9.vCDZ7lw59UUEliWQvF0sMmwVJxXGT2hGyB2H0KFRQJY','2025-02-25 12:36:20.884997','2025-03-04 12:36:20.000000',5,'28c8687308f14cceb90ae88a003b0508'),(137,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTA5NTQwMywiaWF0IjoxNzQwNDkwNjAzLCJqdGkiOiI5NDJmYTUyNTU3MDE0MTQ0YTU4ZGM2NmZiNjFjY2RkMyIsInVzZXJfaWQiOjV9.NPN6VJ9Slv4ovNZCy4Ds7sgS9vY8VRo6oMerdaEt4Fk','2025-02-25 13:36:43.103955','2025-03-04 13:36:43.000000',5,'942fa52557014144a58dc66fb61ccdd3'),(138,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTA5OTA1NCwiaWF0IjoxNzQwNDk0MjU0LCJqdGkiOiIwNTFmZjU3NjE5MDI0OTBhODllMjU0NWFiYWE1ZTU0MiIsInVzZXJfaWQiOjV9.dmiB1ch74iz3dmUfm47bGKd_eMXeU7qENzAoB5A6W40','2025-02-25 14:37:34.218224','2025-03-04 14:37:34.000000',5,'051ff5761902490a89e2545abaa5e542'),(139,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTEwMjkwMiwiaWF0IjoxNzQwNDk4MTAyLCJqdGkiOiI4NWJjYjdmYWJkYWE0M2UyOGE5ODUzNDc3MDMxNmQ2MyIsInVzZXJfaWQiOjV9.eK5zBLnSiCxvGB1K2PPFy5jzUlb2VDZb_E9IpTD8yvI','2025-02-25 15:41:42.286902','2025-03-04 15:41:42.000000',5,'85bcb7fabdaa43e28a98534770316d63'),(140,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTEwNjUzNCwiaWF0IjoxNzQwNTAxNzM0LCJqdGkiOiI2MDQ4YTY3OWExZjU0YmQ2OWJlMWQ5MTZhOWRiZWQ5ZiIsInVzZXJfaWQiOjV9.xmPupP8cQ-16GpSByiyUpfA-kuxMFfrEdgzbTtVG3V0','2025-02-25 16:42:14.051508','2025-03-04 16:42:14.000000',5,'6048a679a1f54bd69be1d916a9dbed9f'),(141,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTExMDY4NCwiaWF0IjoxNzQwNTA1ODg0LCJqdGkiOiJjMTNjYjMxODY1N2I0ODE4YWFlMTViZjVhNjBiNTEyMCIsInVzZXJfaWQiOjV9.EsgH0c4aZ6ivWykK_s9b6gLTOiyQY5hpXxYk_gZibg4','2025-02-25 17:51:24.198671','2025-03-04 17:51:24.000000',5,'c13cb318657b4818aae15bf5a60b5120'),(142,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE1MzY3OSwiaWF0IjoxNzQwNTQ4ODc5LCJqdGkiOiI0YjNjZDY2MzU4ZDY0ODI5OTUwOTVmNmY4NjAwYzFkOCIsInVzZXJfaWQiOjV9.LWfe23zVW_ddeiqSOGSbZb4Kgjn7nYTtV-w3T5X0stw','2025-02-26 05:47:59.981898','2025-03-05 05:47:59.000000',5,'4b3cd66358d6482995095f6f8600c1d8'),(143,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE4MDE3NCwiaWF0IjoxNzQwNTc1Mzc0LCJqdGkiOiI5MDhlZjI3ZGY0Y2I0Nzk5ODFiMGI3M2FhM2JiMzQ3MiIsInVzZXJfaWQiOjV9.Qp1idkBsQKc038nHNNve8rU5lIYdLOq4XfWeU54RSwk','2025-02-26 13:09:34.553129','2025-03-05 13:09:34.000000',5,'908ef27df4cb479981b0b73aa3bb3472'),(144,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE4NDIxNCwiaWF0IjoxNzQwNTc5NDE0LCJqdGkiOiJiMDc5OWM2NDJlNDQ0ZDllODQzOTBmZDQxMzQ0NmQ0MCIsInVzZXJfaWQiOjV9.Y7l4Q3uEh6X-NOmO1fd8OqWNGm_udyxsXvcLUmQ6r_A','2025-02-26 14:16:54.268651','2025-03-05 14:16:54.000000',5,'b0799c642e444d9e84390fd413446d40'),(145,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE4Nzk0OSwiaWF0IjoxNzQwNTgzMTQ5LCJqdGkiOiI2YThlOWUwZWY3MWU0Mzg1OGNkMDIxZWFiMWZlNjExOCIsInVzZXJfaWQiOjV9.wL40YJR5XsQxt3wOfpbgZe5X8q1uZafCqp72OTsGOHI','2025-02-26 15:19:09.596766','2025-03-05 15:19:09.000000',5,'6a8e9e0ef71e43858cd021eab1fe6118'),(146,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE4OTI4NiwiaWF0IjoxNzQwNTg0NDg2LCJqdGkiOiIzNGZmYWQxZWI5NDY0OWNhYWEzMzc0Mzk2MDk4MTUzMyJ9.dwQJY_tAhFhJP5j6DGVVtTofEs5LzPbK6S3AjR0Av9w','2025-02-26 15:41:26.969553','2025-03-05 15:41:26.000000',NULL,'34ffad1eb94649caaa33743960981533'),(147,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE4OTI5MSwiaWF0IjoxNzQwNTg0NDkxLCJqdGkiOiIxMjQ4MmNkYzU2OWI0YWUxYTY2MjhmZjNlNWQ1OWZmOCIsInVzZXJfaWQiOjV9.B1Iyhvbd5wVtl_kANZeLCFP1kSnRK5MVO2H2Mpz7aMU','2025-02-26 15:41:31.637268','2025-03-05 15:41:31.000000',5,'12482cdc569b4ae1a6628ff3e5d59ff8'),(148,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE5Mjk3MywiaWF0IjoxNzQwNTg4MTczLCJqdGkiOiJhNjdkYjkzNTNjZGU0MDIwOGZjZDQ1MDc4OWZkMmI1ZiIsInVzZXJfaWQiOjV9.3ZuyAp-nGgowEtLB0QlpEP4IXULklJHC2dBFo9NOeu0','2025-02-26 16:42:53.343283','2025-03-05 16:42:53.000000',5,'a67db9353cde40208fcd450789fd2b5f'),(149,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE5NjY1MSwiaWF0IjoxNzQwNTkxODUxLCJqdGkiOiI0NmI3OTE5NmFmOGQ0MWExOWFlZWFjMzY3OWRhOWZlNCIsInVzZXJfaWQiOjV9.4DkrWpm9NXd-yIrZMHLSspYgtm1oKaAm6ZvVA9yImMg','2025-02-26 17:44:11.956920','2025-03-05 17:44:11.000000',5,'46b79196af8d41a19aeeac3679da9fe4'),(150,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTIwMDQ5NSwiaWF0IjoxNzQwNTk1Njk1LCJqdGkiOiIwMjA1YTZhNTdmZWQ0MWIzYjlmYTkwZDQzNTZlNGVjYiIsInVzZXJfaWQiOjV9.LD_LqZK7iicHM0C8xLHXbGPf7iZ42IVoJ3NSqSlX4w8','2025-02-26 18:48:15.841511','2025-03-05 18:48:15.000000',5,'0205a6a57fed41b3b9fa90d4356e4ecb'),(151,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTIyMTU4MCwiaWF0IjoxNzQwNjE2NzgwLCJqdGkiOiI4NDEzYzdhNzhhMmU0ODUwOWNiNGFkM2I5YTc5OGM2ZCIsInVzZXJfaWQiOjV9.4kmAczQvSXecp4Nd9w0bAp0JY5rs34b-WGbao5SL16M','2025-02-27 00:39:40.947518','2025-03-06 00:39:40.000000',5,'8413c7a78a2e48509cb4ad3b9a798c6d'),(152,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTIyMjc0MiwiaWF0IjoxNzQwNjE3OTQyLCJqdGkiOiIyYmMzYzYzODMxYWY0NTdiOGFjZGE3YTI1ZjMyNmY5MiIsInVzZXJfaWQiOjV9.HdxYNBXpO37gJ6zGFe7ZX25Wt6bs_K7JABHdxJkJKJ0','2025-02-27 00:59:02.933527','2025-03-06 00:59:02.000000',5,'2bc3c63831af457b8acda7a25f326f92'),(153,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTIzNTQ3NCwiaWF0IjoxNzQwNjMwNjc0LCJqdGkiOiI0OGRmZjFiMmQ3YzM0ODFhYmQyMDRhMmNiZGYwMThmOCIsInVzZXJfaWQiOjV9.76sVe2TJH6P4L-sJyogA9f1QzC4H2bAug5BeSifn_Ms','2025-02-27 04:31:14.134208','2025-03-06 04:31:14.000000',5,'48dff1b2d7c3481abd204a2cbdf018f8'),(154,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTIzNTgwNiwiaWF0IjoxNzQwNjMxMDA2LCJqdGkiOiI3NjlmYTQwMTBhMTQ0MGY3OWYzM2YzNDBiM2JhZDBhZCJ9.ejX4C4rYw2kWhH6SsZaaKvqh-cxTcECZgraGvUG7aP8','2025-02-27 04:36:46.734409','2025-03-06 04:36:46.000000',NULL,'769fa4010a1440f79f33f340b3bad0ad'),(155,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTIzNTgxMSwiaWF0IjoxNzQwNjMxMDExLCJqdGkiOiI5NjFkNmMyMjcxMGM0MjA2OTQ0MzY5YTQwMjkxNzVlMyIsInVzZXJfaWQiOjV9.P4Kcp86iqihNcrj5RDg5ktAzOzJMso75Y752CouZ0TU','2025-02-27 04:36:51.864175','2025-03-06 04:36:51.000000',5,'961d6c22710c4206944369a4029175e3'),(156,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTIzNjg0OSwiaWF0IjoxNzQwNjMyMDQ5LCJqdGkiOiI5YTU0N2Y3ODc0YWQ0ZDY0YjgzM2Q5MjM0N2Q0NWIyNCIsInVzZXJfaWQiOjV9.S1aJI2-79WDXWsURVbk84xuzZLzB3T2uQoXoQKwKuXo','2025-02-27 04:54:09.824347','2025-03-06 04:54:09.000000',5,'9a547f7874ad4d64b833d92347d45b24'),(157,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTIzNjg4NCwiaWF0IjoxNzQwNjMyMDg0LCJqdGkiOiI5N2RhZDg2MTA3NDE0N2M2YmI3NTNmMzg0MzVlMDdmYyIsInVzZXJfaWQiOjV9.ZrOMaFIHwpYfjsx9In5SaGcBu7Ro2R-xXGlngYwg0vI','2025-02-27 04:54:44.699806','2025-03-06 04:54:44.000000',5,'97dad861074147c6bb753f38435e07fc'),(158,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTIzNzAxMiwiaWF0IjoxNzQwNjMyMjEyLCJqdGkiOiJiMzEzZGE2ZGEzODU0MTQ3YTFhMDJmZjYzNGY3MzI0MiIsInVzZXJfaWQiOjV9.SyaOna2RwzOhslYI1oU2oz9m3UikPbdVlbZVdkI6Ru0','2025-02-27 04:56:52.823622','2025-03-06 04:56:52.000000',5,'b313da6da3854147a1a02ff634f73242'),(159,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTIzNzA5OCwiaWF0IjoxNzQwNjMyMjk4LCJqdGkiOiJmNTU4NWFlNmE0YjY0MDUzYTQzN2FjYmU3NzcyYTZkMSIsInVzZXJfaWQiOjV9.T7qFJoZY1nF4vL3OIATd7-eijFu-VsjxMcgd058DgMg','2025-02-27 04:58:18.950849','2025-03-06 04:58:18.000000',5,'f5585ae6a4b64053a437acbe7772a6d1'),(160,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTIzNzE0NywiaWF0IjoxNzQwNjMyMzQ3LCJqdGkiOiJjMGQwOTg1NGRhZTM0YTQ1YmU5MWM1NTE2ZWQxZmRlNSJ9.Gjk3bq33I8eroS2TVQd3zZutxhy_Gpy8IT2w7bXvlVA','2025-02-27 04:59:07.078757','2025-03-06 04:59:07.000000',NULL,'c0d09854dae34a45be91c5516ed1fde5'),(161,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTIzNzE1MCwiaWF0IjoxNzQwNjMyMzUwLCJqdGkiOiIzYzFhZGQ1ODJlZGE0ZWFjOTc3MzZiY2FmNmVhMjhlNCIsInVzZXJfaWQiOjV9.fTRqwFf5vQHFtdfpdFyLCmDYfy7Naeia74e7erw01wU','2025-02-27 04:59:10.141977','2025-03-06 04:59:10.000000',5,'3c1add582eda4eac97736bcaf6ea28e4'),(162,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTI0MTE0MSwiaWF0IjoxNzQwNjM2MzQxLCJqdGkiOiI1NjYwMmVlNmJhMWM0NTFkYTg4YjgwZmIzZWNiN2Y2NyIsInVzZXJfaWQiOjV9.ArjUOdfXueTnjtaGR7RbkH0F3ILQLiEiNk3dpa_Wwns','2025-02-27 06:05:41.294247','2025-03-06 06:05:41.000000',5,'56602ee6ba1c451da88b80fb3ecb7f67'),(163,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTI0NTI3MiwiaWF0IjoxNzQwNjQwNDcyLCJqdGkiOiIwYzZlNjc5YzcwOTk0MTdlOTYxYmQxYmQ5MjhjNDA3NCIsInVzZXJfaWQiOjV9.SoUkYmeHqPRK-OJ_tUZQo3s7tqqg1CwASO-szNG7yEQ','2025-02-27 07:14:32.944473','2025-03-06 07:14:32.000000',5,'0c6e679c7099417e961bd1bd928c4074'),(164,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTI0OTI2MiwiaWF0IjoxNzQwNjQ0NDYyLCJqdGkiOiI1ZGE1YjRkZWE5MTA0YWJjYjE2OTc3ODM4MTFkZWYwZiIsInVzZXJfaWQiOjV9.ix2G4C4flbTfSr5WksHHXUYDIMYoa7aSNvLMdlG3Tqo','2025-02-27 08:21:02.706780','2025-03-06 08:21:02.000000',5,'5da5b4dea9104abcb1697783811def0f'),(165,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTI1NTIxNSwiaWF0IjoxNzQwNjUwNDE1LCJqdGkiOiI4NWM0NTIwZjBiOGM0MDlkYjgwMWM1NzliZjFiZjQ4ZCIsInVzZXJfaWQiOjV9.EUSKhadA9rxx15FpGsX1jmOTuGfOATP9yuzkQtMKktY','2025-02-27 10:00:15.583469','2025-03-06 10:00:15.000000',5,'85c4520f0b8c409db801c579bf1bf48d'),(166,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTI2NTM5MiwiaWF0IjoxNzQwNjYwNTkyLCJqdGkiOiJkOTU5M2M0MzE3OGM0OTI2YmY1ZmYxMjU3OGFiYjhlMCIsInVzZXJfaWQiOjV9.a6qTG933AwmSkJTv2t3rOj8WTdmzShDXCVs5V5-r_WY','2025-02-27 12:49:52.771548','2025-03-06 12:49:52.000000',5,'d9593c43178c4926bf5ff12578abb8e0'),(167,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTI3MDQwNCwiaWF0IjoxNzQwNjY1NjA0LCJqdGkiOiI2NjZiOTA5NDgzNDE0ZWQxOWZjMzg5NDA4YWY0ZmFhZiIsInVzZXJfaWQiOjV9.cQw9OfBXggvLZFU2AnO3QjuYI1113-70E6NjJmCRA5o','2025-02-27 14:13:24.386924','2025-03-06 14:13:24.000000',5,'666b909483414ed19fc389408af4faaf'),(168,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTI3NDIzMSwiaWF0IjoxNzQwNjY5NDMxLCJqdGkiOiIxYzBiNjc4YTIzNjU0NjJlYTQ5YmI4Yzc3OWZmZjI2NiIsInVzZXJfaWQiOjV9.v_R7P28iqeD1XoHznq2O5qV4UfoRqS-KWoL9PfsAWYI','2025-02-27 15:17:11.906561','2025-03-06 15:17:11.000000',5,'1c0b678a2365462ea49bb8c779fff266'),(169,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTI3NzcwMCwiaWF0IjoxNzQwNjcyOTAwLCJqdGkiOiI0OTNkNjMzZTI3YjQ0OTI0YTg5N2UzZGJlMTlhNTYwMiIsInVzZXJfaWQiOjV9.dE7TJHQFxLeuFKvrN_24KxnlLGaGnszFhP-8qLbZN0o','2025-02-27 16:15:00.917100','2025-03-06 16:15:00.000000',5,'493d633e27b44924a897e3dbe19a5602'),(170,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTI4NTkxNSwiaWF0IjoxNzQwNjgxMTE1LCJqdGkiOiJkZjU4NmFiYWNjNjc0ODk3OGRkZTQ0ZDI3MjZjMGQ0YSIsInVzZXJfaWQiOjV9.zto0oMiVD0H0Ez1HZ2oQukINBtU72_IJiL1SUDCQbuw','2025-02-27 18:31:55.557994','2025-03-06 18:31:55.000000',5,'df586abacc6748978dde44d2726c0d4a'),(171,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTMxMTM0MiwiaWF0IjoxNzQwNzA2NTQyLCJqdGkiOiI0NDljZjdhNzQ0ZDg0MWJjOWI2NTg1ODVkM2I3YTYyNSIsInVzZXJfaWQiOjV9.N_Td2Qn_t8DOBndw5OKzC2OnIjGH-wQAEDJpsZhXZpQ','2025-02-28 01:35:42.272969','2025-03-07 01:35:42.000000',5,'449cf7a744d841bc9b658585d3b7a625'),(172,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTMxODI4MCwiaWF0IjoxNzQwNzEzNDgwLCJqdGkiOiI4NjY3NjlmYWMzNzk0OWRhYWMyNzM3NmU3YmI3NTgzZiIsInVzZXJfaWQiOjV9.9vTsUw4N3ebo--oxQbqk1VMzGJJfiKIE1oaZpSnGlVU','2025-02-28 03:31:20.027240','2025-03-07 03:31:20.000000',5,'866769fac37949daac27376e7bb7583f'),(173,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTMyMzI3MiwiaWF0IjoxNzQwNzE4NDcyLCJqdGkiOiI1NDliYTZlY2U3OWE0YzVhOGY1YmM3MmJkY2M2ZTdlZSIsInVzZXJfaWQiOjV9.QqGoyMx6X_EulZqQ-AQLnOtmolgCD7mOW0o0ZfeChOw','2025-02-28 04:54:32.143156','2025-03-07 04:54:32.000000',5,'549ba6ece79a4c5a8f5bc72bdcc6e7ee'),(174,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTM0MDMzNywiaWF0IjoxNzQwNzM1NTM3LCJqdGkiOiI1Y2I1OTkwMGJmYjY0YzZkYTkwODdiMzU1NzIxNTJkNCIsInVzZXJfaWQiOjV9.8k5kuUGufGB1PCPyiPes24yClsgXYDG3WBGKI5BA0rg','2025-02-28 09:38:57.612264','2025-03-07 09:38:57.000000',5,'5cb59900bfb64c6da9087b35572152d4');
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` ENABLE KEYS */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `family_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `given_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `picture` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `profile_picture` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `users_email_0ea73cca_uniq` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (5,'pbkdf2_sha256$720000$oGNAgLA2HywZW5jy9aSKto$K736OT8kHdYn8gZ3sUmwZtE400j95VYTf6XnHgRPSHQ=',NULL,1,'toshiki','','','th.osigoto0719@gmail.com',1,1,'2025-02-10 04:36:40.968580','2025-02-10 04:36:41.170345','2025-02-10 04:36:41.170345',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

--
-- Table structure for table `users_groups`
--

DROP TABLE IF EXISTS `users_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_groups_user_id_group_id_fc7788e8_uniq` (`user_id`,`group_id`),
  KEY `users_groups_group_id_2f3517aa_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_groups_user_id_f500bee5_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_groups`
--

/*!40000 ALTER TABLE `users_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_groups` ENABLE KEYS */;

--
-- Table structure for table `users_user_permissions`
--

DROP TABLE IF EXISTS `users_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_permissions_user_id_permission_id_3b86cbdf_uniq` (`user_id`,`permission_id`),
  KEY `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_permissions_user_id_92473840_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_permissions`
--

/*!40000 ALTER TABLE `users_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_permissions` ENABLE KEYS */;

--
-- Dumping routines for database 'market_king'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-28 20:03:20
