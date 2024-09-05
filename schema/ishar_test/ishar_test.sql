-- MySQL dump 10.13  Distrib 8.3.0, for macos14.2 (x86_64)
--
-- Host: 127.0.0.1    Database: ishar_test
-- ------------------------------------------------------
-- Server version	5.5.5-10.7.8-MariaDB-1:10.7.8+maria~ubu2004-log

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
-- Table structure for table `account_achievements`
--

DROP TABLE IF EXISTS `account_achievements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_achievements` (
  `account_achievement_id` int(11) NOT NULL AUTO_INCREMENT,
  `achievement_id` int(11) DEFAULT NULL,
  `is_completed` tinyint(1) DEFAULT 0,
  `completion_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `account_id` int(10) unsigned DEFAULT NULL,
  `completed_by` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`account_achievement_id`),
  UNIQUE KEY `account_achievements_unique` (`achievement_id`,`account_id`),
  KEY `account_achievements_accounts_FK` (`account_id`),
  CONSTRAINT `account_achievements_accounts_FK` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `account_achievements_achievements_FK` FOREIGN KEY (`achievement_id`) REFERENCES `achievements` (`achievement_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4303 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `account_backup`
--

DROP TABLE IF EXISTS `account_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_backup` (
  `account_id` int(11) unsigned NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `current_essence` mediumint(4) unsigned NOT NULL DEFAULT 0,
  `email` varchar(30) NOT NULL,
  `password` varchar(36) NOT NULL,
  `create_isp` varchar(25) NOT NULL,
  `last_isp` varchar(25) NOT NULL,
  `create_ident` varchar(25) NOT NULL,
  `last_ident` varchar(25) NOT NULL,
  `create_haddr` int(11) NOT NULL,
  `last_haddr` int(11) NOT NULL,
  `account_name` varchar(25) NOT NULL,
  `account_gift` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `banned_until` timestamp NULL DEFAULT NULL,
  `bugs_reported` int(11) NOT NULL DEFAULT 0,
  `earned_essence` mediumint(9) NOT NULL DEFAULT 0,
  `immortal_level` smallint(6) DEFAULT 0,
  `is_private` tinyint(1) DEFAULT 0,
  `comm` int(11) DEFAULT 0,
  `achievement_points` int(10) unsigned DEFAULT 0,
  `beta_tester` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `account_soulbound_items`
--

DROP TABLE IF EXISTS `account_soulbound_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_soulbound_items` (
  `account_soulbound_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `item_id` int(10) unsigned DEFAULT NULL,
  `cooldown` int(10) unsigned DEFAULT 0,
  `last_used` timestamp NULL DEFAULT current_timestamp(),
  `time_gained` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `account_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`account_soulbound_id`),
  UNIQUE KEY `account_soulbound_items_unique` (`item_id`,`account_id`),
  KEY `account_soulbound_items_accounts_FK` (`account_id`),
  CONSTRAINT `account_soulbound_items_accounts_FK` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=537 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `account_titles`
--

DROP TABLE IF EXISTS `account_titles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_titles` (
  `account_titles_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `account_id` int(10) unsigned DEFAULT NULL,
  `title_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`account_titles_id`),
  KEY `account_titles_accounts_FK` (`account_id`),
  KEY `account_titles_titles_FK` (`title_id`),
  CONSTRAINT `account_titles_accounts_FK` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `account_titles_titles_FK` FOREIGN KEY (`title_id`) REFERENCES `titles` (`title_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `account_upgrades`
--

DROP TABLE IF EXISTS `account_upgrades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_upgrades` (
  `id` tinyint(4) unsigned NOT NULL,
  `cost` mediumint(4) unsigned NOT NULL,
  `description` varchar(400) NOT NULL,
  `name` varchar(80) NOT NULL,
  `max_value` mediumint(4) unsigned NOT NULL DEFAULT 1,
  `scale` tinyint(4) NOT NULL DEFAULT 1,
  `is_disabled` tinyint(1) NOT NULL DEFAULT 0,
  `increment` tinyint(4) NOT NULL,
  `amount` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_upgrades_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `account_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `current_essence` mediumint(4) unsigned NOT NULL DEFAULT 0,
  `email` varchar(30) NOT NULL,
  `password` varchar(36) NOT NULL,
  `create_isp` varchar(25) NOT NULL,
  `last_isp` varchar(25) NOT NULL,
  `create_ident` varchar(25) NOT NULL,
  `last_ident` varchar(25) NOT NULL,
  `create_haddr` int(11) NOT NULL,
  `last_haddr` int(11) NOT NULL,
  `account_name` varchar(25) NOT NULL,
  `account_gift` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `banned_until` timestamp NULL DEFAULT NULL,
  `bugs_reported` int(11) NOT NULL DEFAULT 0,
  `earned_essence` mediumint(9) NOT NULL DEFAULT 0,
  `is_private` tinyint(1) DEFAULT 0,
  `immortal_level` smallint(6) DEFAULT 0,
  `comm` int(11) DEFAULT 0,
  `achievement_points` int(10) unsigned DEFAULT 0,
  `beta_tester` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `account_name` (`account_name`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=21776 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `accounts_account_upgrades`
--

DROP TABLE IF EXISTS `accounts_account_upgrades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_account_upgrades` (
  `account_upgrades_id` tinyint(4) unsigned NOT NULL,
  `account_id` int(11) unsigned NOT NULL,
  `amount` mediumint(4) unsigned NOT NULL,
  PRIMARY KEY (`account_upgrades_id`,`account_id`),
  KEY `account_upgrades_id` (`account_upgrades_id`),
  KEY `accounts_account_id` (`account_id`),
  CONSTRAINT `account_upgrades_id` FOREIGN KEY (`account_upgrades_id`) REFERENCES `account_upgrades` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `accounts_account_id` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `accounts_configuration_options`
--

DROP TABLE IF EXISTS `accounts_configuration_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_configuration_options` (
  `account_id` int(11) unsigned NOT NULL,
  `configuration_option_id` tinyint(4) unsigned NOT NULL,
  `value` varchar(76) NOT NULL,
  PRIMARY KEY (`account_id`,`configuration_option_id`),
  KEY `accounts_configuration_options_id` (`configuration_option_id`),
  CONSTRAINT `accounts_configuration_account_id` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `accounts_configuration_options_id` FOREIGN KEY (`configuration_option_id`) REFERENCES `configuration_options` (`configuration_option_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `achievement_class_restrict`
--

DROP TABLE IF EXISTS `achievement_class_restrict`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `achievement_class_restrict` (
  `acr_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `achievement_id` int(11) DEFAULT NULL,
  `class_id` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`acr_id`),
  KEY `achievement_class_restrict_achievements_FK` (`achievement_id`),
  KEY `achievement_class_restrict_classes_FK` (`class_id`),
  CONSTRAINT `achievement_class_restrict_achievements_FK` FOREIGN KEY (`achievement_id`) REFERENCES `achievements` (`achievement_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `achievement_class_restrict_classes_FK` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `achievement_criteria`
--

DROP TABLE IF EXISTS `achievement_criteria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `achievement_criteria` (
  `criteria_id` int(11) NOT NULL AUTO_INCREMENT,
  `achievement_id` int(11) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `criteria_type` varchar(32) DEFAULT NULL,
  `target_value` varchar(10) DEFAULT '0',
  `group_id` tinyint(3) unsigned DEFAULT 0,
  PRIMARY KEY (`criteria_id`),
  KEY `achievement_id` (`achievement_id`),
  CONSTRAINT `achievement_criteria_ibfk_1` FOREIGN KEY (`achievement_id`) REFERENCES `achievements` (`achievement_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `achievement_rewards`
--

DROP TABLE IF EXISTS `achievement_rewards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `achievement_rewards` (
  `reward_id` int(11) NOT NULL AUTO_INCREMENT,
  `achievement_id` int(11) DEFAULT NULL,
  `reward_type` int(10) unsigned DEFAULT NULL,
  `reward_value` int(11) DEFAULT NULL,
  PRIMARY KEY (`reward_id`),
  KEY `achievement_id` (`achievement_id`),
  CONSTRAINT `achievement_rewards_ibfk_1` FOREIGN KEY (`achievement_id`) REFERENCES `achievements` (`achievement_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `achievement_triggers`
--

DROP TABLE IF EXISTS `achievement_triggers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `achievement_triggers` (
  `achievement_triggers_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `achievement_id` int(11) DEFAULT NULL,
  `trigger_type` enum('LEVEL_UP','REMORT','GAIN_RENOWN','DEATH','QUEST_COMPLETE','CHALLENGE_COMPLETE') NOT NULL,
  PRIMARY KEY (`achievement_triggers_id`),
  KEY `achievement_triggers_achievements_FK` (`achievement_id`),
  CONSTRAINT `achievement_triggers_achievements_FK` FOREIGN KEY (`achievement_id`) REFERENCES `achievements` (`achievement_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `achievements`
--

DROP TABLE IF EXISTS `achievements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `achievements` (
  `achievement_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `is_hidden` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `category` varchar(80) DEFAULT NULL,
  `parent_category` varchar(80) DEFAULT NULL,
  `ordinal` int(11) DEFAULT -1,
  `criteria_type` enum('PlayerOnly','Account','AccountGrouped','AccountTotal') DEFAULT NULL,
  PRIMARY KEY (`achievement_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `admin_interface_theme`
--

DROP TABLE IF EXISTS `admin_interface_theme`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_interface_theme` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `title` varchar(50) NOT NULL,
  `title_visible` tinyint(1) NOT NULL,
  `logo` varchar(100) NOT NULL,
  `logo_visible` tinyint(1) NOT NULL,
  `css_header_background_color` varchar(10) NOT NULL,
  `title_color` varchar(10) NOT NULL,
  `css_header_text_color` varchar(10) NOT NULL,
  `css_header_link_color` varchar(10) NOT NULL,
  `css_header_link_hover_color` varchar(10) NOT NULL,
  `css_module_background_color` varchar(10) NOT NULL,
  `css_module_text_color` varchar(10) NOT NULL,
  `css_module_link_color` varchar(10) NOT NULL,
  `css_module_link_hover_color` varchar(10) NOT NULL,
  `css_module_rounded_corners` tinyint(1) NOT NULL,
  `css_generic_link_color` varchar(10) NOT NULL,
  `css_generic_link_hover_color` varchar(10) NOT NULL,
  `css_save_button_background_color` varchar(10) NOT NULL,
  `css_save_button_background_hover_color` varchar(10) NOT NULL,
  `css_save_button_text_color` varchar(10) NOT NULL,
  `css_delete_button_background_color` varchar(10) NOT NULL,
  `css_delete_button_background_hover_color` varchar(10) NOT NULL,
  `css_delete_button_text_color` varchar(10) NOT NULL,
  `list_filter_dropdown` tinyint(1) NOT NULL,
  `related_modal_active` tinyint(1) NOT NULL,
  `related_modal_background_color` varchar(10) NOT NULL,
  `related_modal_rounded_corners` tinyint(1) NOT NULL,
  `logo_color` varchar(10) NOT NULL,
  `recent_actions_visible` tinyint(1) NOT NULL,
  `favicon` varchar(100) NOT NULL,
  `related_modal_background_opacity` varchar(5) NOT NULL,
  `env_name` varchar(50) NOT NULL,
  `env_visible_in_header` tinyint(1) NOT NULL,
  `env_color` varchar(10) NOT NULL,
  `env_visible_in_favicon` tinyint(1) NOT NULL,
  `related_modal_close_button_visible` tinyint(1) NOT NULL,
  `language_chooser_active` tinyint(1) NOT NULL,
  `language_chooser_display` varchar(10) NOT NULL,
  `list_filter_sticky` tinyint(1) NOT NULL,
  `form_pagination_sticky` tinyint(1) NOT NULL,
  `form_submit_sticky` tinyint(1) NOT NULL,
  `css_module_background_selected_color` varchar(10) NOT NULL,
  `css_module_link_selected_color` varchar(10) NOT NULL,
  `logo_max_height` smallint(5) unsigned NOT NULL CHECK (`logo_max_height` >= 0),
  `logo_max_width` smallint(5) unsigned NOT NULL CHECK (`logo_max_width` >= 0),
  `foldable_apps` tinyint(1) NOT NULL,
  `language_chooser_control` varchar(20) NOT NULL,
  `list_filter_highlight` tinyint(1) NOT NULL,
  `list_filter_removal_links` tinyint(1) NOT NULL,
  `show_fieldsets_as_tabs` tinyint(1) NOT NULL,
  `show_inlines_as_tabs` tinyint(1) NOT NULL,
  `css_generic_link_active_color` varchar(10) NOT NULL,
  `collapsible_stacked_inlines` tinyint(1) NOT NULL,
  `collapsible_stacked_inlines_collapsed` tinyint(1) NOT NULL,
  `collapsible_tabular_inlines` tinyint(1) NOT NULL,
  `collapsible_tabular_inlines_collapsed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `admin_interface_theme_name_30bda70f_uniq` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `affect_flags`
--

DROP TABLE IF EXISTS `affect_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `affect_flags` (
  `flag_id` tinyint(4) unsigned NOT NULL,
  `name` varchar(30) NOT NULL,
  `display_name` varchar(100) NOT NULL,
  `is_beneficial` tinyint(1) DEFAULT 0,
  `item_description` varchar(100) NOT NULL,
  PRIMARY KEY (`flag_id`),
  UNIQUE KEY `affect_flag_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `areas`
--

DROP TABLE IF EXISTS `areas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `areas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `min_level` smallint(6) NOT NULL,
  `max_level` smallint(6) NOT NULL,
  `group_size` smallint(6) NOT NULL,
  `zone_num` smallint(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=309 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_accounts_account_id` FOREIGN KEY (`user_id`) REFERENCES `accounts` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `boards`
--

DROP TABLE IF EXISTS `boards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `boards` (
  `board_id` tinyint(4) unsigned NOT NULL,
  `board_name` varchar(15) NOT NULL,
  PRIMARY KEY (`board_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `challenges`
--

DROP TABLE IF EXISTS `challenges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `challenges` (
  `challenge_id` smallint(4) NOT NULL AUTO_INCREMENT,
  `mob_vnum` int(10) unsigned NOT NULL,
  `max_level` tinyint(4) NOT NULL,
  `max_people` tinyint(4) NOT NULL,
  `chall_tier` tinyint(4) NOT NULL,
  `challenge_desc` varchar(80) NOT NULL,
  `winner_desc` varchar(80) NOT NULL DEFAULT '--',
  `mob_name` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 0,
  `last_completion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `num_completed` int(11) NOT NULL DEFAULT 0,
  `num_picked` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`challenge_id`),
  KEY `challenges_mob_data_FK` (`mob_vnum`),
  CONSTRAINT `challenges_mob_data_FK` FOREIGN KEY (`mob_vnum`) REFERENCES `mob_data` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=259 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `class_levels`
--

DROP TABLE IF EXISTS `class_levels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_levels` (
  `class_level_id` int(11) NOT NULL AUTO_INCREMENT,
  `level` tinyint(4) NOT NULL,
  `male_title` varchar(80) NOT NULL,
  `female_title` varchar(80) NOT NULL,
  `class_id` tinyint(3) unsigned NOT NULL,
  `experience` int(11) NOT NULL,
  PRIMARY KEY (`class_level_id`),
  KEY `class_levels_class_id` (`class_id`),
  CONSTRAINT `class_levels_class_id` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `class_skills`
--

DROP TABLE IF EXISTS `class_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_skills` (
  `class_skills_id` int(11) NOT NULL AUTO_INCREMENT,
  `class_id` tinyint(3) unsigned NOT NULL,
  `skill_id` int(11) NOT NULL,
  `min_level` int(11) NOT NULL,
  `max_learn` tinyint(4) NOT NULL,
  `auto_learn` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`class_skills_id`),
  KEY `class_skills_class_id` (`class_id`),
  KEY `class_skills_skill_id` (`skill_id`),
  CONSTRAINT `class_skills_class_id` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `class_skills_skill_id` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=256 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classes` (
  `class_id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `class_name` varchar(15) NOT NULL DEFAULT 'NO_CLASS',
  `class_display` varchar(32) DEFAULT NULL,
  `class_description` varchar(80) DEFAULT NULL,
  `is_playable` tinyint(1) NOT NULL DEFAULT 0,
  `base_hit_pts` int(11) NOT NULL,
  `hit_pts_per_level` int(11) NOT NULL,
  `attack_per_level` int(11) NOT NULL,
  `spell_rate` int(11) NOT NULL,
  `class_stat` tinyint(4) NOT NULL,
  `class_dc` int(11) NOT NULL,
  `base_fortitude` int(11) NOT NULL,
  `base_resilience` int(11) NOT NULL,
  `base_reflex` int(11) NOT NULL,
  PRIMARY KEY (`class_id`),
  UNIQUE KEY `class_name` (`class_name`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `classes_races`
--

DROP TABLE IF EXISTS `classes_races`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classes_races` (
  `classes_races_id` int(11) NOT NULL AUTO_INCREMENT,
  `race_id` int(11) NOT NULL,
  `class_id` tinyint(11) unsigned NOT NULL,
  PRIMARY KEY (`classes_races_id`),
  KEY `races_race_id` (`race_id`),
  KEY `classes_class_id` (`class_id`),
  CONSTRAINT `classes_class_id` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `races_race_id` FOREIGN KEY (`race_id`) REFERENCES `races` (`race_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `conditions`
--

DROP TABLE IF EXISTS `conditions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conditions` (
  `condition_id` tinyint(4) unsigned NOT NULL,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`condition_id`),
  UNIQUE KEY `condition_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `configuration_options`
--

DROP TABLE IF EXISTS `configuration_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `configuration_options` (
  `configuration_option_id` tinyint(4) unsigned NOT NULL,
  `name` varchar(20) NOT NULL,
  `is_display` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`configuration_option_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_account_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_account_id` FOREIGN KEY (`user_id`) REFERENCES `accounts` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=441 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_flatpage`
--

DROP TABLE IF EXISTS `django_flatpage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_flatpage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `enable_comments` tinyint(1) NOT NULL,
  `template_name` varchar(70) NOT NULL,
  `registration_required` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_flatpage_url_41612362` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_flatpage_sites`
--

DROP TABLE IF EXISTS `django_flatpage_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_flatpage_sites` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `flatpage_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_flatpage_sites_flatpage_id_site_id_0d29d9d1_uniq` (`flatpage_id`,`site_id`),
  KEY `django_flatpage_sites_site_id_bfd8ea84_fk_django_site_id` (`site_id`),
  CONSTRAINT `django_flatpage_sites_flatpage_id_078bbc8b_fk_django_flatpage_id` FOREIGN KEY (`flatpage_id`) REFERENCES `django_flatpage` (`id`),
  CONSTRAINT `django_flatpage_sites_site_id_bfd8ea84_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `faqs`
--

DROP TABLE IF EXISTS `faqs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faqs` (
  `faq_id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `question_text` longtext NOT NULL,
  `question_answer` longtext NOT NULL,
  `is_visible` tinyint(1) NOT NULL,
  `display_order` int(10) unsigned NOT NULL CHECK (`display_order` >= 0),
  `account_id` int(10) unsigned NOT NULL,
  `slug` varchar(16) NOT NULL,
  PRIMARY KEY (`faq_id`),
  UNIQUE KEY `display_order` (`display_order`),
  UNIQUE KEY `slug` (`slug`),
  KEY `faqs_account_id_4743be56_fk_accounts_account_id` (`account_id`),
  CONSTRAINT `faqs_account_id_4743be56_fk_accounts_account_id` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forces`
--

DROP TABLE IF EXISTS `forces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forces` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `force_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `force_name` (`force_name`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_event`
--

DROP TABLE IF EXISTS `global_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `global_event` (
  `event_type` tinyint(4) NOT NULL,
  `start_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `end_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `event_name` varchar(20) NOT NULL,
  `event_desc` varchar(40) NOT NULL,
  `xp_bonus` tinyint(4) NOT NULL DEFAULT 0,
  `shop_bonus` tinyint(4) NOT NULL,
  `celestial_luck` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`event_type`),
  UNIQUE KEY `global_event_event_type_IDX` (`event_type`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `historic_season_stat`
--

DROP TABLE IF EXISTS `historic_season_stat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historic_season_stat` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `season_id` int(10) unsigned DEFAULT NULL,
  `account_id` int(10) unsigned DEFAULT NULL,
  `player_name` varchar(100) DEFAULT NULL,
  `remorts` mediumint(8) unsigned DEFAULT NULL,
  `class_id` tinyint(3) unsigned DEFAULT NULL,
  `race_id` int(11) DEFAULT NULL,
  `total_renown` mediumint(8) unsigned DEFAULT NULL,
  `challenges_completed` mediumint(8) unsigned DEFAULT NULL,
  `quests_completed` mediumint(8) unsigned DEFAULT NULL,
  `deaths` mediumint(8) unsigned DEFAULT NULL,
  `game_type` tinyint(3) unsigned DEFAULT NULL,
  `play_time` int(10) unsigned DEFAULT NULL,
  `level` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `historic_season_stat_accounts_FK` (`account_id`),
  KEY `historic_season_stat_seasons_FK` (`season_id`),
  KEY `historic_season_stat_classes_FK` (`class_id`),
  KEY `historic_season_stat_races_FK` (`race_id`),
  CONSTRAINT `historic_season_stat_accounts_FK` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `historic_season_stat_classes_FK` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `historic_season_stat_races_FK` FOREIGN KEY (`race_id`) REFERENCES `races` (`race_id`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `historic_season_stat_seasons_FK` FOREIGN KEY (`season_id`) REFERENCES `seasons` (`season_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=720 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kill_memory`
--

DROP TABLE IF EXISTS `kill_memory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kill_memory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `player_id` int(10) unsigned DEFAULT NULL,
  `kill_memory_set` int(11) DEFAULT NULL,
  `scratch` smallint(6) DEFAULT NULL,
  `nonzero` smallint(6) DEFAULT NULL,
  `total` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `player_id` (`player_id`,`kill_memory_set`),
  CONSTRAINT `kill_memory_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=535477 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kill_memory_buckets`
--

DROP TABLE IF EXISTS `kill_memory_buckets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kill_memory_buckets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kill_memory_id` int(11) DEFAULT NULL,
  `bucket_index` smallint(6) DEFAULT NULL,
  `value` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `kill_memory_id` (`kill_memory_id`,`bucket_index`),
  CONSTRAINT `kill_memory_buckets_ibfk_1` FOREIGN KEY (`kill_memory_id`) REFERENCES `kill_memory` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=233685168 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mob_affect_flags`
--

DROP TABLE IF EXISTS `mob_affect_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mob_affect_flags` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `mob_id` int(10) unsigned DEFAULT NULL,
  `flag_id` tinyint(3) unsigned DEFAULT NULL,
  `value` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mob_affect_flags_unique` (`mob_id`,`flag_id`),
  KEY `mob_affect_flags_affect_flags_FK` (`flag_id`),
  CONSTRAINT `mob_affect_flags_affect_flags_FK` FOREIGN KEY (`flag_id`) REFERENCES `affect_flags` (`flag_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mob_affect_flags_mob_data_FK` FOREIGN KEY (`mob_id`) REFERENCES `mob_data` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=727335 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mob_data`
--

DROP TABLE IF EXISTS `mob_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mob_data` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `long_name` varchar(100) NOT NULL,
  `room_desc` varchar(100) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `spec_func` varchar(100) DEFAULT NULL,
  `position` tinyint(3) unsigned DEFAULT 10,
  `l_position` tinyint(3) unsigned DEFAULT NULL,
  `damage_dice_number` smallint(5) unsigned DEFAULT NULL,
  `damage_dice_size` smallint(5) unsigned DEFAULT NULL,
  `extra_armor` smallint(6) DEFAULT NULL,
  `additional_health_heal` smallint(6) DEFAULT 0,
  `additional_move_heal` smallint(6) DEFAULT 0,
  `additional_mana_heal` smallint(6) DEFAULT 0,
  `additional_favor_heal` smallint(6) DEFAULT 0,
  `additional_damage` smallint(6) DEFAULT 0,
  `additional_speed` smallint(6) DEFAULT 0,
  `additional_alignment` mediumint(9) DEFAULT 0,
  `armor` mediumint(9) DEFAULT 0,
  `attack` mediumint(9) DEFAULT 0,
  `sex` tinyint(3) unsigned DEFAULT NULL,
  `race_id` int(11) DEFAULT NULL,
  `class_id` tinyint(3) unsigned DEFAULT NULL,
  `level` tinyint(3) unsigned DEFAULT 0,
  `weight` smallint(5) unsigned NOT NULL,
  `height` smallint(5) unsigned NOT NULL,
  `comm_points` smallint(6) NOT NULL,
  `alignment` smallint(6) NOT NULL,
  `strength` tinyint(3) unsigned NOT NULL,
  `agility` tinyint(3) unsigned NOT NULL,
  `endurance` tinyint(3) unsigned NOT NULL,
  `perception` tinyint(3) unsigned NOT NULL,
  `focus` tinyint(3) unsigned NOT NULL,
  `willpower` tinyint(3) unsigned NOT NULL,
  `init_strength` tinyint(3) unsigned NOT NULL,
  `init_agility` tinyint(3) unsigned NOT NULL,
  `init_endurance` tinyint(3) unsigned NOT NULL,
  `init_perception` tinyint(3) unsigned NOT NULL,
  `init_focus` tinyint(3) unsigned NOT NULL,
  `init_willpower` tinyint(3) unsigned NOT NULL,
  `perm_hit_pts` smallint(6) NOT NULL,
  `perm_move_pts` smallint(6) NOT NULL,
  `perm_spell_pts` smallint(6) NOT NULL,
  `perm_favor_pts` smallint(6) NOT NULL,
  `curr_hit_pts` smallint(6) NOT NULL,
  `curr_move_pts` smallint(6) NOT NULL,
  `curr_spell_pts` smallint(6) NOT NULL,
  `curr_favor_pts` smallint(6) NOT NULL,
  `experience` int(11) NOT NULL,
  `gold` mediumint(9) NOT NULL,
  `karma` mediumint(9) NOT NULL,
  `hrange_low` int(11) DEFAULT NULL,
  `hrange_high` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_deleted` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `mob_data_classes_FK` (`class_id`),
  KEY `mob_data_races_FK` (`race_id`),
  CONSTRAINT `mob_data_classes_FK` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`),
  CONSTRAINT `mob_data_races_FK` FOREIGN KEY (`race_id`) REFERENCES `races` (`race_id`)
) ENGINE=InnoDB AUTO_INCREMENT=100002 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mob_extra_descriptions`
--

DROP TABLE IF EXISTS `mob_extra_descriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mob_extra_descriptions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `mob_id` int(10) unsigned DEFAULT NULL,
  `extra_name` varchar(100) DEFAULT NULL,
  `extra_description` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mob_extra_descriptions_unique` (`mob_id`,`extra_name`),
  CONSTRAINT `mob_extra_descriptions_mob_data_FK_1` FOREIGN KEY (`mob_id`) REFERENCES `mob_data` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=70256 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mob_player_flags`
--

DROP TABLE IF EXISTS `mob_player_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mob_player_flags` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `mob_id` int(10) unsigned DEFAULT NULL,
  `flag_id` int(10) unsigned DEFAULT NULL,
  `value` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mob_player_flags_unique` (`mob_id`,`flag_id`),
  KEY `mob_player_flags_player_flags_FK` (`flag_id`),
  CONSTRAINT `mob_player_flags_mob_data_FK` FOREIGN KEY (`mob_id`) REFERENCES `mob_data` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mob_player_flags_player_flags_FK` FOREIGN KEY (`flag_id`) REFERENCES `player_flags` (`flag_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2351329 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mob_stats`
--

DROP TABLE IF EXISTS `mob_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mob_stats` (
  `mob_stats_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `mob_id` int(10) unsigned DEFAULT NULL,
  `num_loaded_all` int(10) unsigned DEFAULT 0,
  `num_loaded_season` int(10) unsigned DEFAULT 0,
  `num_killed_all` int(10) unsigned DEFAULT 0,
  `num_killed_season` int(10) unsigned DEFAULT 0,
  `num_pc_killed_all` int(10) unsigned DEFAULT 0,
  `num_pc_killed_season` int(10) unsigned DEFAULT 0,
  `num_encountered_all` int(10) unsigned DEFAULT 0,
  `num_encountered_season` int(10) unsigned DEFAULT NULL,
  `num_fled_all` int(10) unsigned DEFAULT 0,
  `num_fled_season` int(10) unsigned DEFAULT 0,
  PRIMARY KEY (`mob_stats_id`),
  KEY `mob_stats_mob_data_FK` (`mob_id`),
  CONSTRAINT `mob_stats_mob_data_FK` FOREIGN KEY (`mob_id`) REFERENCES `mob_data` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1656694 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mud_client_categories`
--

DROP TABLE IF EXISTS `mud_client_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mud_client_categories` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `is_visible` tinyint(1) NOT NULL,
  `display_order` int(10) unsigned NOT NULL CHECK (`display_order` >= 0),
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `display_order` (`display_order`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mud_clients`
--

DROP TABLE IF EXISTS `mud_clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mud_clients` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `url` varchar(200) NOT NULL,
  `is_visible` tinyint(1) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`client_id`),
  UNIQUE KEY `name` (`name`),
  KEY `mud_clients_category_id_b8f9988d_fk_mud_clien` (`category_id`),
  CONSTRAINT `mud_clients_category_id_b8f9988d_fk_mud_clien` FOREIGN KEY (`category_id`) REFERENCES `mud_client_categories` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mud_processes`
--

DROP TABLE IF EXISTS `mud_processes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mud_processes` (
  `process_id` int(10) unsigned NOT NULL CHECK (`process_id` >= 0),
  `name` varchar(32) NOT NULL,
  `user` varchar(32) NOT NULL,
  `last_updated` datetime(6) NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`process_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `news` (
  `news_id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `subject` varchar(64) NOT NULL,
  `body` longtext NOT NULL,
  `is_visible` tinyint(1) NOT NULL,
  `account_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`news_id`),
  KEY `news_account_id_a97d4dc6_fk_accounts_account_id` (`account_id`),
  CONSTRAINT `news_account_id_a97d4dc6_fk_accounts_account_id` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `object_affect_flags`
--

DROP TABLE IF EXISTS `object_affect_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `object_affect_flags` (
  `object_vnum` int(10) unsigned NOT NULL,
  `affect_flag_id` tinyint(3) unsigned NOT NULL,
  `value` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`affect_flag_id`,`object_vnum`),
  KEY `fk_object_affect_flags_object_vnum` (`object_vnum`),
  CONSTRAINT `fk_object_affect_flags_affect_flag_id` FOREIGN KEY (`affect_flag_id`) REFERENCES `affect_flags` (`flag_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_object_affect_flags_object_vnum` FOREIGN KEY (`object_vnum`) REFERENCES `objects` (`vnum`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `object_extras`
--

DROP TABLE IF EXISTS `object_extras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `object_extras` (
  `object_vnum` int(10) unsigned NOT NULL,
  `keywords` varchar(128) NOT NULL,
  `description` varchar(4096) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`object_vnum`,`keywords`),
  CONSTRAINT `fk_object_extras_object_vnum` FOREIGN KEY (`object_vnum`) REFERENCES `objects` (`vnum`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `object_flags`
--

DROP TABLE IF EXISTS `object_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `object_flags` (
  `object_vnum` int(10) unsigned NOT NULL,
  `MAGIC` tinyint(1) NOT NULL DEFAULT 0,
  `CURSED` tinyint(1) NOT NULL DEFAULT 0,
  `DONATED` tinyint(1) NOT NULL DEFAULT 0,
  `NOTGOOD` tinyint(1) NOT NULL DEFAULT 0,
  `NOTEVIL` tinyint(1) NOT NULL DEFAULT 0,
  `NOTNEUTRAL` tinyint(1) NOT NULL DEFAULT 0,
  `INVISIBLE` tinyint(1) NOT NULL DEFAULT 0,
  `MOVED` tinyint(1) NOT NULL DEFAULT 0,
  `NOTWARRIOR` tinyint(1) NOT NULL DEFAULT 0,
  `NOTROGUE` tinyint(1) NOT NULL DEFAULT 0,
  `NOTCLERIC` tinyint(1) NOT NULL DEFAULT 0,
  `NOTMAGICIAN` tinyint(1) NOT NULL DEFAULT 0,
  `TRAPPED` tinyint(1) NOT NULL DEFAULT 0,
  `SURFACE` tinyint(1) NOT NULL DEFAULT 0,
  `HIGH_RENT` tinyint(1) NOT NULL DEFAULT 0,
  `NOTMORTALS` tinyint(1) NOT NULL DEFAULT 0,
  `DAY_DECAY` tinyint(1) NOT NULL DEFAULT 0,
  `ENCHANTED` tinyint(1) NOT NULL DEFAULT 0,
  `RENTED` tinyint(1) NOT NULL DEFAULT 0,
  `POSSESSED` tinyint(1) NOT NULL DEFAULT 0,
  `PERSISTENT` tinyint(1) NOT NULL DEFAULT 0,
  `MODIFIED` tinyint(1) NOT NULL DEFAULT 0,
  `IN_EDIT` tinyint(1) NOT NULL DEFAULT 0,
  `REMOVE_OBJ` tinyint(1) NOT NULL DEFAULT 0,
  `CONTROLLED` tinyint(1) NOT NULL DEFAULT 0,
  `NOIDENT` tinyint(1) NOT NULL DEFAULT 0,
  `UNRENTABLE` tinyint(1) NOT NULL DEFAULT 0,
  `NOLOCATE` tinyint(1) NOT NULL DEFAULT 0,
  `ARTIFACT` tinyint(1) NOT NULL DEFAULT 0,
  `QUEST_OBJ` tinyint(1) NOT NULL DEFAULT 0,
  `EMP_ENCHANT` tinyint(1) NOT NULL DEFAULT 0,
  `QUEST_SOURCE` tinyint(1) NOT NULL DEFAULT 0,
  `NOT_SHAMAN` tinyint(1) NOT NULL DEFAULT 0,
  `RELIC` tinyint(1) DEFAULT 0,
  `MEMORY` tinyint(1) DEFAULT 0,
  `NOTNECROMANCER` tinyint(1) DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`object_vnum`),
  CONSTRAINT `fk_object_flags_object_vnum` FOREIGN KEY (`object_vnum`) REFERENCES `objects` (`vnum`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `object_mods`
--

DROP TABLE IF EXISTS `object_mods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `object_mods` (
  `mod_id` int(10) unsigned NOT NULL,
  `name` varchar(30) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`mod_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `object_object_mods`
--

DROP TABLE IF EXISTS `object_object_mods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `object_object_mods` (
  `object_vnum` int(10) unsigned NOT NULL,
  `mod_slot` int(10) unsigned NOT NULL DEFAULT 0,
  `object_mod_id` int(10) unsigned NOT NULL,
  `value` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`object_vnum`,`mod_slot`),
  KEY `fk_object_object_mods_object_mod_id` (`object_mod_id`),
  CONSTRAINT `fk_object_object_mods_object_mod_id` FOREIGN KEY (`object_mod_id`) REFERENCES `object_mods` (`mod_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_object_object_mods_object_vnum` FOREIGN KEY (`object_vnum`) REFERENCES `objects` (`vnum`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `object_wearable_flags`
--

DROP TABLE IF EXISTS `object_wearable_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `object_wearable_flags` (
  `object_vnum` int(10) unsigned NOT NULL,
  `TAKE` tinyint(1) NOT NULL DEFAULT 0,
  `WIELD` tinyint(1) NOT NULL DEFAULT 0,
  `HOLD` tinyint(1) NOT NULL DEFAULT 0,
  `TWO_HANDS` tinyint(1) NOT NULL DEFAULT 0,
  `BODY` tinyint(1) NOT NULL DEFAULT 0,
  `HEAD` tinyint(1) NOT NULL DEFAULT 0,
  `NECK` tinyint(1) NOT NULL DEFAULT 0,
  `CHEST` tinyint(1) NOT NULL DEFAULT 0,
  `BACK` tinyint(1) NOT NULL DEFAULT 0,
  `ARMS` tinyint(1) NOT NULL DEFAULT 0,
  `WRIST` tinyint(1) NOT NULL DEFAULT 0,
  `HANDS` tinyint(1) NOT NULL DEFAULT 0,
  `FINGER` tinyint(1) NOT NULL DEFAULT 0,
  `WAIST` tinyint(1) NOT NULL DEFAULT 0,
  `LEGS` tinyint(1) NOT NULL DEFAULT 0,
  `FEET` tinyint(1) NOT NULL DEFAULT 0,
  `ABOUT` tinyint(1) NOT NULL DEFAULT 0,
  `SHIELD` tinyint(1) NOT NULL DEFAULT 0,
  `FACE` tinyint(1) NOT NULL DEFAULT 0,
  `MOUTH` tinyint(1) NOT NULL DEFAULT 0,
  `FORE_MARK` tinyint(1) NOT NULL DEFAULT 0,
  `UPPER_BODY` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`object_vnum`),
  CONSTRAINT `fk_object_wearable_flags_object_vnum` FOREIGN KEY (`object_vnum`) REFERENCES `objects` (`vnum`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `objects`
--

DROP TABLE IF EXISTS `objects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `objects` (
  `vnum` int(10) unsigned NOT NULL,
  `name` varchar(128) DEFAULT NULL,
  `longname` varchar(256) DEFAULT NULL,
  `appearance` varchar(256) DEFAULT NULL,
  `description` varchar(8192) DEFAULT NULL,
  `func` varchar(128) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `timer` smallint(6) DEFAULT NULL,
  `enchant` int(11) DEFAULT NULL,
  `item_type` tinyint(4) DEFAULT NULL,
  `equipped` tinyint(3) unsigned DEFAULT NULL,
  `size` smallint(6) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `value` int(11) DEFAULT 0,
  `val0` int(11) DEFAULT NULL,
  `val1` int(11) DEFAULT NULL,
  `val2` int(11) DEFAULT NULL,
  `val3` int(11) DEFAULT NULL,
  `deleted` tinyint(4) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `calculated_value` int(11) DEFAULT 0,
  PRIMARY KEY (`vnum`),
  KEY `objects_skills_FK` (`enchant`),
  CONSTRAINT `objects_skills_FK` FOREIGN KEY (`enchant`) REFERENCES `skills` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `patches`
--

DROP TABLE IF EXISTS `patches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patches` (
  `patch_id` int(11) NOT NULL AUTO_INCREMENT,
  `patch_date` datetime(6) NOT NULL,
  `patch_name` varchar(64) NOT NULL,
  `patch_file` varchar(100) NOT NULL,
  `is_visible` tinyint(1) NOT NULL,
  `account_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`patch_id`),
  UNIQUE KEY `patch_name` (`patch_name`),
  KEY `patches_account_id_9dd7e888_fk_accounts_account_id` (`account_id`),
  CONSTRAINT `patches_account_id_9dd7e888_fk_accounts_account_id` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_affects`
--

DROP TABLE IF EXISTS `player_affects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_affects` (
  `player_affect_id` int(11) NOT NULL AUTO_INCREMENT,
  `player_id` int(10) unsigned NOT NULL,
  `affect_id` int(11) NOT NULL,
  `expires` int(11) NOT NULL,
  `bits` int(11) NOT NULL,
  `location_1` int(11) NOT NULL,
  `mod_1` int(11) NOT NULL,
  `location_2` int(11) NOT NULL,
  `mod_2` int(11) NOT NULL,
  `aflags_blob` varbinary(128) DEFAULT NULL,
  PRIMARY KEY (`player_affect_id`),
  UNIQUE KEY `player_affect_unique` (`player_id`,`affect_id`),
  KEY `player_affects_ibfk_2` (`affect_id`),
  CONSTRAINT `player_affects_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE,
  CONSTRAINT `player_affects_ibfk_2` FOREIGN KEY (`affect_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=29081 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_backup`
--

DROP TABLE IF EXISTS `player_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_backup` (
  `id` int(11) unsigned NOT NULL DEFAULT 0,
  `account_id` int(11) unsigned NOT NULL,
  `name` varchar(15) NOT NULL DEFAULT '',
  `create_ident` varchar(10) NOT NULL DEFAULT '',
  `last_isp` varchar(30) NOT NULL DEFAULT '',
  `description` varchar(240) DEFAULT NULL,
  `title` varchar(45) NOT NULL DEFAULT '',
  `poofin` varchar(80) NOT NULL DEFAULT '',
  `poofout` varchar(80) NOT NULL DEFAULT '',
  `bankacc` int(11) unsigned NOT NULL,
  `logon_delay` smallint(6) unsigned NOT NULL,
  `true_level` tinyint(3) unsigned NOT NULL,
  `renown` smallint(5) unsigned NOT NULL,
  `remorts` tinyint(3) unsigned NOT NULL,
  `favors` tinyint(3) unsigned NOT NULL,
  `online` int(11) DEFAULT NULL,
  `bound_room` int(11) unsigned NOT NULL,
  `load_room` int(11) unsigned NOT NULL,
  `invstart_level` int(11) DEFAULT NULL,
  `login_failures` smallint(6) unsigned NOT NULL,
  `create_haddr` int(11) NOT NULL,
  `login_fail_haddr` int(11) DEFAULT NULL,
  `last_haddr` int(11) DEFAULT NULL,
  `last_ident` varchar(10) DEFAULT '',
  `load_room_next` int(11) unsigned DEFAULT NULL,
  `load_room_next_expires` int(11) unsigned DEFAULT NULL,
  `aggro_until` int(11) unsigned DEFAULT NULL,
  `inn_limit` smallint(6) unsigned NOT NULL,
  `held_xp` int(11) DEFAULT NULL,
  `last_isp_change` int(11) unsigned DEFAULT NULL,
  `is_deleted` tinyint(4) unsigned NOT NULL DEFAULT 0,
  `deaths` smallint(5) unsigned NOT NULL DEFAULT 0,
  `total_renown` smallint(5) unsigned NOT NULL DEFAULT 0,
  `quests_completed` smallint(5) unsigned NOT NULL DEFAULT 0,
  `challenges_completed` smallint(5) unsigned NOT NULL DEFAULT 0,
  `game_type` tinyint(4) NOT NULL DEFAULT 0,
  `birth` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `logon` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `logout` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `title_id` int(10) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_boards`
--

DROP TABLE IF EXISTS `player_boards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_boards` (
  `player_id` int(11) unsigned NOT NULL,
  `board_id` tinyint(4) unsigned NOT NULL,
  `last_read` tinyint(4) NOT NULL,
  `last_read_time` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`player_id`,`board_id`),
  KEY `player_boards_player_id` (`player_id`),
  KEY `player_boards_board_id` (`board_id`),
  CONSTRAINT `boards_board_id` FOREIGN KEY (`board_id`) REFERENCES `boards` (`board_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `players_id` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_challenges`
--

DROP TABLE IF EXISTS `player_challenges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_challenges` (
  `player_id` int(11) unsigned NOT NULL,
  `challenge_id` smallint(4) NOT NULL,
  `last_completed` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `player_challenges_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `num_completed_cycle` tinyint(3) unsigned DEFAULT 0,
  `num_completed_all` tinyint(3) unsigned DEFAULT 0,
  PRIMARY KEY (`player_challenges_id`),
  UNIQUE KEY `player_id` (`player_id`,`challenge_id`),
  KEY `player_challenges_cid` (`challenge_id`),
  CONSTRAINT `player_challenges_cid` FOREIGN KEY (`challenge_id`) REFERENCES `challenges` (`challenge_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `player_challenges_pid` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_common`
--

DROP TABLE IF EXISTS `player_common`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_common` (
  `player_id` int(11) unsigned NOT NULL,
  `class_id` tinyint(4) NOT NULL,
  `race_id` int(11) NOT NULL,
  `sex` tinyint(4) NOT NULL DEFAULT 0,
  `level` tinyint(3) unsigned NOT NULL,
  `weight` smallint(5) unsigned NOT NULL,
  `height` smallint(5) unsigned NOT NULL,
  `comm_points` smallint(6) NOT NULL,
  `alignment` smallint(6) NOT NULL,
  `strength` tinyint(3) unsigned NOT NULL,
  `agility` tinyint(3) unsigned NOT NULL,
  `endurance` tinyint(3) unsigned NOT NULL,
  `perception` tinyint(3) unsigned NOT NULL,
  `focus` tinyint(3) unsigned NOT NULL,
  `willpower` tinyint(3) unsigned NOT NULL,
  `init_strength` tinyint(3) unsigned NOT NULL,
  `init_agility` tinyint(3) unsigned NOT NULL,
  `init_endurance` tinyint(3) unsigned NOT NULL,
  `init_perception` tinyint(3) unsigned NOT NULL,
  `init_focus` tinyint(3) unsigned NOT NULL,
  `init_willpower` tinyint(3) unsigned NOT NULL,
  `perm_hit_pts` smallint(6) NOT NULL,
  `perm_move_pts` smallint(6) NOT NULL,
  `perm_spell_pts` smallint(6) NOT NULL,
  `perm_favor_pts` smallint(6) NOT NULL,
  `curr_hit_pts` smallint(6) NOT NULL,
  `curr_move_pts` smallint(6) NOT NULL,
  `curr_spell_pts` smallint(6) NOT NULL,
  `curr_favor_pts` smallint(6) NOT NULL,
  `experience` int(11) NOT NULL,
  `gold` mediumint(9) NOT NULL,
  `karma` mediumint(9) NOT NULL,
  UNIQUE KEY `pc_player_id` (`player_id`),
  KEY `player_common_player_id` (`player_id`),
  KEY `player_common_race_id` (`race_id`),
  CONSTRAINT `player_common_player_id` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `player_common_race_id` FOREIGN KEY (`race_id`) REFERENCES `races` (`race_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_common_backup`
--

DROP TABLE IF EXISTS `player_common_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_common_backup` (
  `player_id` int(11) unsigned NOT NULL,
  `class_id` tinyint(4) NOT NULL,
  `race_id` int(11) NOT NULL,
  `sex` tinyint(4) NOT NULL DEFAULT 0,
  `level` tinyint(3) unsigned NOT NULL,
  `weight` smallint(5) unsigned NOT NULL,
  `height` smallint(5) unsigned NOT NULL,
  `comm_points` smallint(6) NOT NULL,
  `alignment` smallint(6) NOT NULL,
  `strength` tinyint(3) unsigned NOT NULL,
  `agility` tinyint(3) unsigned NOT NULL,
  `endurance` tinyint(3) unsigned NOT NULL,
  `perception` tinyint(3) unsigned NOT NULL,
  `focus` tinyint(3) unsigned NOT NULL,
  `willpower` tinyint(3) unsigned NOT NULL,
  `init_strength` tinyint(3) unsigned NOT NULL,
  `init_agility` tinyint(3) unsigned NOT NULL,
  `init_endurance` tinyint(3) unsigned NOT NULL,
  `init_perception` tinyint(3) unsigned NOT NULL,
  `init_focus` tinyint(3) unsigned NOT NULL,
  `init_willpower` tinyint(3) unsigned NOT NULL,
  `perm_hit_pts` smallint(6) NOT NULL,
  `perm_move_pts` smallint(6) NOT NULL,
  `perm_spell_pts` smallint(6) NOT NULL,
  `perm_favor_pts` smallint(6) NOT NULL,
  `curr_hit_pts` smallint(6) NOT NULL,
  `curr_move_pts` smallint(6) NOT NULL,
  `curr_spell_pts` smallint(6) NOT NULL,
  `curr_favor_pts` smallint(6) NOT NULL,
  `experience` int(11) NOT NULL,
  `gold` mediumint(9) NOT NULL,
  `karma` mediumint(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_conditions`
--

DROP TABLE IF EXISTS `player_conditions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_conditions` (
  `player_id` int(11) unsigned NOT NULL,
  `condition_id` tinyint(4) unsigned NOT NULL,
  `value` smallint(6) unsigned NOT NULL,
  PRIMARY KEY (`player_id`,`condition_id`),
  KEY `player_condition_condition_id` (`condition_id`),
  KEY `player_condition_player_id` (`player_id`),
  CONSTRAINT `conditions_condition_id` FOREIGN KEY (`condition_id`) REFERENCES `conditions` (`condition_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `player_id` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_configuration_options`
--

DROP TABLE IF EXISTS `player_configuration_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_configuration_options` (
  `player_id` int(11) unsigned NOT NULL,
  `configuration_option_id` tinyint(4) unsigned NOT NULL,
  `value` varchar(76) NOT NULL,
  PRIMARY KEY (`player_id`,`configuration_option_id`),
  KEY `player_id` (`player_id`),
  KEY `player_display_options_display_id` (`configuration_option_id`) USING BTREE,
  CONSTRAINT `player_display_options_display_id` FOREIGN KEY (`configuration_option_id`) REFERENCES `configuration_options` (`configuration_option_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `player_display_options_player_id` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_flags`
--

DROP TABLE IF EXISTS `player_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_flags` (
  `flag_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`flag_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_objects`
--

DROP TABLE IF EXISTS `player_objects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_objects` (
  `player_objects_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `player_id` int(10) unsigned DEFAULT NULL,
  `object_id` int(10) unsigned DEFAULT NULL,
  `enchant` int(10) unsigned DEFAULT NULL,
  `timer` int(11) DEFAULT NULL,
  `bound` int(10) unsigned DEFAULT NULL,
  `state` int(10) unsigned DEFAULT NULL,
  `min_level` tinyint(3) unsigned DEFAULT 0,
  `val0` int(11) DEFAULT NULL,
  `val1` int(11) DEFAULT NULL,
  `val2` int(11) DEFAULT NULL,
  `val3` int(11) DEFAULT NULL,
  `position_type` tinyint(3) unsigned DEFAULT NULL,
  `position_val` tinyint(4) DEFAULT NULL,
  `parent_player_object` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`player_objects_id`),
  KEY `player_objects_players_FK` (`player_id`),
  KEY `player_objects_objects_FK` (`object_id`),
  KEY `player_objects_player_objects_FK` (`parent_player_object`),
  CONSTRAINT `player_objects_objects_FK` FOREIGN KEY (`object_id`) REFERENCES `objects` (`vnum`),
  CONSTRAINT `player_objects_players_FK` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5197 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_player_flags`
--

DROP TABLE IF EXISTS `player_player_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_player_flags` (
  `flag_id` int(11) unsigned NOT NULL,
  `player_id` int(11) unsigned NOT NULL,
  `value` int(11) unsigned NOT NULL,
  PRIMARY KEY (`flag_id`,`player_id`),
  KEY `player_player_flags_flag_id` (`flag_id`),
  KEY `player_player_flags_player_id` (`player_id`),
  CONSTRAINT `player_player_flags_flag_id` FOREIGN KEY (`flag_id`) REFERENCES `player_flags` (`flag_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `player_player_flags_player_id` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_quest_steps`
--

DROP TABLE IF EXISTS `player_quest_steps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_quest_steps` (
  `player_id` int(11) unsigned NOT NULL,
  `step_id` tinyint(4) NOT NULL,
  `num_collected` tinyint(1) NOT NULL,
  PRIMARY KEY (`player_id`,`step_id`),
  KEY `player_steps_step_id` (`step_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_quests`
--

DROP TABLE IF EXISTS `player_quests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_quests` (
  `quest_id` int(11) unsigned NOT NULL,
  `player_id` int(11) unsigned NOT NULL,
  `status` tinyint(11) NOT NULL DEFAULT -2,
  `last_completed_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `num_completed` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`quest_id`,`player_id`),
  KEY `player_quests_player_id` (`player_id`),
  KEY `player_id_index` (`player_id`),
  CONSTRAINT `player_quests_player_id` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `player_quests_quest_id` FOREIGN KEY (`quest_id`) REFERENCES `quests` (`quest_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_relics`
--

DROP TABLE IF EXISTS `player_relics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_relics` (
  `player_id` int(10) unsigned NOT NULL,
  `obj_vnum` int(10) unsigned NOT NULL,
  UNIQUE KEY `player_id` (`player_id`,`obj_vnum`),
  CONSTRAINT `player_relics_player_id` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_remort_upgrades`
--

DROP TABLE IF EXISTS `player_remort_upgrades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_remort_upgrades` (
  `upgrade_id` int(11) unsigned NOT NULL,
  `player_id` int(11) unsigned NOT NULL,
  `value` int(11) unsigned NOT NULL,
  `essence_perk` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`upgrade_id`,`player_id`),
  KEY `player_remote_upgrades_upgrade_id` (`upgrade_id`),
  KEY `player_remote_upgrades_player_id` (`player_id`),
  CONSTRAINT `player_remote_upgrades_player_id` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `player_remote_upgrades_upgrade_id` FOREIGN KEY (`upgrade_id`) REFERENCES `remort_upgrades` (`upgrade_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_skills`
--

DROP TABLE IF EXISTS `player_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_skills` (
  `skill_id` int(11) NOT NULL,
  `player_id` int(11) unsigned NOT NULL,
  `skill_level` tinyint(11) unsigned NOT NULL,
  PRIMARY KEY (`skill_id`,`player_id`),
  KEY `player_skills_player_id` (`player_id`),
  CONSTRAINT `player_skills_player_id` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `player_skills_skill_id` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_stats`
--

DROP TABLE IF EXISTS `player_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_stats` (
  `player_stats_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `player_id` int(10) unsigned DEFAULT NULL,
  `total_play_time` int(10) unsigned DEFAULT NULL,
  `remort_play_time` int(10) unsigned DEFAULT NULL,
  `total_deaths` mediumint(8) unsigned DEFAULT 0,
  `remort_deaths` mediumint(8) unsigned DEFAULT 0,
  `total_renown` int(10) unsigned DEFAULT NULL,
  `remort_renown` int(10) unsigned DEFAULT NULL,
  `total_challenges` int(10) unsigned DEFAULT NULL,
  `remort_challenges` int(10) unsigned DEFAULT NULL,
  `total_quests` int(10) unsigned DEFAULT NULL,
  `remort_quests` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`player_stats_id`),
  UNIQUE KEY `player_stats_unique` (`player_id`),
  CONSTRAINT `player_stats_players_FK` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4971 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `players` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `account_id` int(11) unsigned NOT NULL,
  `name` varchar(15) NOT NULL DEFAULT '',
  `create_ident` varchar(10) NOT NULL DEFAULT '',
  `last_isp` varchar(30) NOT NULL DEFAULT '',
  `description` varchar(240) DEFAULT NULL,
  `title` varchar(45) NOT NULL DEFAULT '',
  `poofin` varchar(80) NOT NULL DEFAULT '',
  `poofout` varchar(80) NOT NULL DEFAULT '',
  `bankacc` int(11) unsigned NOT NULL,
  `logon_delay` smallint(6) unsigned NOT NULL,
  `true_level` tinyint(3) unsigned NOT NULL,
  `renown` smallint(5) unsigned NOT NULL,
  `remorts` tinyint(3) unsigned NOT NULL,
  `favors` tinyint(3) unsigned NOT NULL,
  `online` int(11) DEFAULT NULL,
  `bound_room` int(11) unsigned NOT NULL,
  `load_room` int(11) unsigned NOT NULL,
  `invstart_level` int(11) DEFAULT NULL,
  `login_failures` smallint(6) unsigned NOT NULL,
  `create_haddr` int(11) NOT NULL,
  `login_fail_haddr` int(11) DEFAULT NULL,
  `last_haddr` int(11) DEFAULT NULL,
  `last_ident` varchar(10) DEFAULT '',
  `load_room_next` int(11) unsigned DEFAULT NULL,
  `load_room_next_expires` int(11) unsigned DEFAULT NULL,
  `aggro_until` int(11) unsigned DEFAULT NULL,
  `inn_limit` smallint(6) unsigned NOT NULL,
  `held_xp` int(11) DEFAULT NULL,
  `last_isp_change` int(11) unsigned DEFAULT NULL,
  `is_deleted` tinyint(4) unsigned NOT NULL DEFAULT 0,
  `deaths` smallint(5) unsigned NOT NULL DEFAULT 0,
  `total_renown` smallint(5) unsigned NOT NULL DEFAULT 0,
  `quests_completed` smallint(5) unsigned NOT NULL DEFAULT 0,
  `challenges_completed` smallint(5) unsigned NOT NULL DEFAULT 0,
  `game_type` tinyint(4) NOT NULL DEFAULT 0,
  `birth` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `logon` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `logout` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `title_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `players_name` (`name`),
  KEY `players_accounts_account_id` (`account_id`),
  KEY `account_id` (`account_id`),
  KEY `players_titles_FK` (`title_id`),
  CONSTRAINT `players_accounts_account_id` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `players_titles_FK` FOREIGN KEY (`title_id`) REFERENCES `titles` (`title_id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=328045 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quest_prereqs`
--

DROP TABLE IF EXISTS `quest_prereqs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quest_prereqs` (
  `quest_id` int(11) unsigned NOT NULL,
  `required_quest` int(11) unsigned NOT NULL,
  `quest_prereqs_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  UNIQUE KEY `id` (`quest_prereqs_id`) USING BTREE,
  UNIQUE KEY `quest_required_quest` (`quest_id`,`required_quest`) USING BTREE,
  KEY `quest_prereqs_required_id` (`required_quest`),
  CONSTRAINT `quest_prereqs_quest_id` FOREIGN KEY (`quest_id`) REFERENCES `quests` (`quest_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `quest_prereqs_required_id` FOREIGN KEY (`required_quest`) REFERENCES `quests` (`quest_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quest_rewards`
--

DROP TABLE IF EXISTS `quest_rewards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quest_rewards` (
  `reward_num` int(11) NOT NULL,
  `reward_type` tinyint(2) NOT NULL,
  `quest_id` int(11) unsigned NOT NULL,
  `class_restrict` tinyint(4) NOT NULL DEFAULT -1,
  `quest_reward_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`quest_reward_id`),
  KEY `quests_rewards_quest_id` (`quest_id`),
  CONSTRAINT `quests_rewards_quest_id` FOREIGN KEY (`quest_id`) REFERENCES `quests` (`quest_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=238 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quest_steps`
--

DROP TABLE IF EXISTS `quest_steps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quest_steps` (
  `step_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `step_type` tinyint(3) NOT NULL,
  `target` int(11) NOT NULL,
  `num_required` int(11) NOT NULL,
  `quest_id` int(11) unsigned NOT NULL,
  `time_limit` int(11) NOT NULL DEFAULT -1,
  `mystify` tinyint(1) NOT NULL DEFAULT 0,
  `mystify_text` varchar(80) NOT NULL DEFAULT '',
  `auto_complete` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`step_id`),
  KEY `quest_steps_quest_id` (`quest_id`),
  CONSTRAINT `quest_steps_quest_id` FOREIGN KEY (`quest_id`) REFERENCES `quests` (`quest_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=176 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quests`
--

DROP TABLE IF EXISTS `quests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quests` (
  `quest_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL DEFAULT '',
  `display_name` varchar(30) NOT NULL,
  `completion_message` varchar(700) NOT NULL,
  `min_level` tinyint(4) NOT NULL DEFAULT 1,
  `max_level` tinyint(4) NOT NULL DEFAULT 20,
  `repeatable` tinyint(1) NOT NULL DEFAULT 0,
  `description` varchar(512) NOT NULL DEFAULT 'No description available.',
  `prerequisite` int(11) NOT NULL DEFAULT -1,
  `class_restrict` tinyint(4) NOT NULL DEFAULT -1,
  `quest_intro` varchar(2000) DEFAULT '',
  `quest_source` int(10) unsigned DEFAULT NULL,
  `quest_return` int(10) unsigned DEFAULT NULL,
  `start_item` int(10) unsigned DEFAULT 0,
  PRIMARY KEY (`quest_id`),
  UNIQUE KEY `quest_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `races`
--

DROP TABLE IF EXISTS `races`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `races` (
  `race_id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(100) DEFAULT '',
  `display_name` varchar(25) DEFAULT '',
  `folk_name` varchar(25) DEFAULT '',
  `default_movement` varchar(10) DEFAULT '',
  `description` varchar(80) DEFAULT '',
  `default_height` smallint(6) DEFAULT 0,
  `default_weight` smallint(6) DEFAULT 0,
  `bonus_fortitude` smallint(6) DEFAULT 0,
  `bonus_reflex` smallint(6) DEFAULT 0,
  `bonus_resilience` smallint(6) DEFAULT 0,
  `listen_sound` varchar(80) DEFAULT '',
  `height_bonus` smallint(6) DEFAULT 0,
  `weight_bonus` smallint(6) DEFAULT 0,
  `short_description` varchar(80) DEFAULT '',
  `long_description` varchar(512) DEFAULT '',
  `attack_noun` varchar(25) DEFAULT '',
  `attack_type` smallint(6) DEFAULT 0,
  `vulnerabilities` text DEFAULT '',
  `susceptibilities` text DEFAULT '',
  `resistances` text DEFAULT '',
  `immunities` text DEFAULT '',
  `additional_str` smallint(6) DEFAULT 0,
  `additional_agi` smallint(6) DEFAULT 0,
  `additional_end` smallint(6) DEFAULT 0,
  `additional_per` smallint(6) DEFAULT 0,
  `additional_foc` smallint(6) DEFAULT 0,
  `additional_wil` smallint(6) DEFAULT 0,
  `is_playable` tinyint(1) DEFAULT 0,
  `is_humanoid` tinyint(1) NOT NULL DEFAULT 1,
  `is_invertebrae` tinyint(1) NOT NULL DEFAULT 0,
  `is_flying` tinyint(1) NOT NULL DEFAULT 0,
  `is_swimming` tinyint(1) NOT NULL DEFAULT 0,
  `darkvision` tinyint(4) NOT NULL DEFAULT 0,
  `see_invis` tinyint(1) NOT NULL DEFAULT 0,
  `is_walking` tinyint(1) NOT NULL DEFAULT 1,
  `endure_heat` tinyint(1) NOT NULL DEFAULT 0,
  `endure_cold` tinyint(1) NOT NULL DEFAULT 0,
  `is_undead` tinyint(1) NOT NULL DEFAULT 0,
  `starting_city` int(10) unsigned DEFAULT 40183,
  `abbr_name` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`race_id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `races_skills`
--

DROP TABLE IF EXISTS `races_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `races_skills` (
  `race_skill_id` int(11) NOT NULL AUTO_INCREMENT,
  `race_id` int(11) NOT NULL,
  `skill_id` int(11) NOT NULL,
  `level` tinyint(4) NOT NULL,
  PRIMARY KEY (`race_skill_id`),
  KEY `races_skills_race_id` (`race_id`),
  KEY `races_skills_skill_id` (`skill_id`),
  CONSTRAINT `races_skills_race_id` FOREIGN KEY (`race_id`) REFERENCES `races` (`race_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `races_skills_skill_id` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `racial_affinities`
--

DROP TABLE IF EXISTS `racial_affinities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `racial_affinities` (
  `race_affinity_id` int(11) NOT NULL AUTO_INCREMENT,
  `race_id` int(11) NOT NULL,
  `force_id` int(11) NOT NULL,
  `affinity_type` tinyint(4) NOT NULL,
  PRIMARY KEY (`race_affinity_id`),
  KEY `racial_affinities_race_id` (`race_id`),
  KEY `racial_affinities_force_id` (`force_id`),
  CONSTRAINT `racial_affinities_force_id` FOREIGN KEY (`force_id`) REFERENCES `forces` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `racial_affinities_race_id` FOREIGN KEY (`race_id`) REFERENCES `races` (`race_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=173 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `racial_deathload`
--

DROP TABLE IF EXISTS `racial_deathload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `racial_deathload` (
  `racial_deathload_id` int(11) NOT NULL AUTO_INCREMENT,
  `race_id` int(11) NOT NULL,
  `vnum` int(11) NOT NULL,
  `percent_chance` int(11) NOT NULL,
  `min_level` int(11) NOT NULL DEFAULT 1,
  `max_level` smallint(5) unsigned DEFAULT 30,
  `max_load` tinyint(3) unsigned DEFAULT 1,
  `class_restrict` tinyint(3) unsigned DEFAULT 4,
  PRIMARY KEY (`racial_deathload_id`),
  KEY `racial_deathload_race_id` (`race_id`),
  KEY `racial_deathload_classes_FK` (`class_restrict`),
  CONSTRAINT `racial_deathload_classes_FK` FOREIGN KEY (`class_restrict`) REFERENCES `classes` (`class_id`),
  CONSTRAINT `racial_deathload_race_id` FOREIGN KEY (`race_id`) REFERENCES `races` (`race_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=389 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `remort_upgrades`
--

DROP TABLE IF EXISTS `remort_upgrades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `remort_upgrades` (
  `upgrade_id` int(11) unsigned NOT NULL,
  `name` varchar(20) NOT NULL DEFAULT '',
  `renown_cost` smallint(6) unsigned NOT NULL,
  `max_value` smallint(6) unsigned NOT NULL,
  `scale` tinyint(4) NOT NULL DEFAULT 10,
  `display_name` varchar(30) NOT NULL,
  `can_buy` tinyint(1) NOT NULL DEFAULT 1,
  `bonus` tinyint(4) NOT NULL DEFAULT 1,
  `survival_scale` tinyint(4) NOT NULL,
  `survival_renown_cost` tinyint(4) NOT NULL,
  PRIMARY KEY (`upgrade_id`),
  UNIQUE KEY `remort_upgrades_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seasons`
--

DROP TABLE IF EXISTS `seasons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seasons` (
  `season_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(4) NOT NULL,
  `effective_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `expiration_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `average_essence_gain` float NOT NULL DEFAULT 0,
  `average_remorts` float NOT NULL DEFAULT 0,
  `max_essence_gain` int(11) NOT NULL DEFAULT 0,
  `max_remorts` int(11) NOT NULL DEFAULT 0,
  `season_leader_account` int(11) NOT NULL DEFAULT 0,
  `seasonal_leader_name` text NOT NULL DEFAULT 'Tyler',
  `last_challenge_cycle` timestamp NOT NULL DEFAULT current_timestamp(),
  `max_renown` int(11) NOT NULL DEFAULT 0,
  `avg_renown` float NOT NULL DEFAULT 0,
  `total_remorts` int(11) NOT NULL DEFAULT 0,
  `game_state` smallint(6) DEFAULT 0,
  `multiplay_limit` smallint(5) unsigned DEFAULT 1,
  PRIMARY KEY (`season_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `skill_components`
--

DROP TABLE IF EXISTS `skill_components`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skill_components` (
  `skill_components_id` int(11) NOT NULL AUTO_INCREMENT,
  `skill_id` int(11) NOT NULL,
  `component_type` int(11) NOT NULL,
  `component_value` int(11) NOT NULL,
  `component_count` smallint(6) DEFAULT 1,
  PRIMARY KEY (`skill_components_id`),
  KEY `skill_components_skills_id` (`skill_id`),
  CONSTRAINT `skill_components_ibfk_1` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=152 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `skill_forces`
--

DROP TABLE IF EXISTS `skill_forces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skill_forces` (
  `skill_id` int(11) NOT NULL,
  `force_id` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `spell_id_2` (`skill_id`,`force_id`),
  KEY `spell_id` (`skill_id`),
  KEY `force_id` (`force_id`),
  CONSTRAINT `skill_forces_ibfk_5` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `skill_forces_ibfk_6` FOREIGN KEY (`force_id`) REFERENCES `forces` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `skill_mods`
--

DROP TABLE IF EXISTS `skill_mods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skill_mods` (
  `skill_mod_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `skill_id` int(11) DEFAULT NULL,
  `mod_location` smallint(6) DEFAULT NULL,
  `mod_value` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`skill_mod_id`),
  KEY `skill_mods_skills_FK` (`skill_id`),
  CONSTRAINT `skill_mods_skills_FK` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `skills`
--

DROP TABLE IF EXISTS `skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skills` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `enum_symbol` varchar(255) NOT NULL,
  `func_name` varchar(255) DEFAULT NULL,
  `skill_name` text DEFAULT NULL,
  `min_posn` int(11) DEFAULT NULL,
  `min_use` int(11) DEFAULT NULL,
  `spell_breakpoint` int(11) DEFAULT NULL,
  `held_cost` int(11) DEFAULT NULL,
  `wearoff_msg` text DEFAULT NULL,
  `chant_text` text DEFAULT NULL,
  `difficulty` int(11) DEFAULT NULL,
  `rate` int(11) DEFAULT NULL,
  `notice_chance` int(11) DEFAULT NULL,
  `appearance` text DEFAULT NULL,
  `scale` int(11) DEFAULT NULL,
  `mod_stat_1` int(11) DEFAULT NULL,
  `mod_stat_2` int(11) DEFAULT NULL,
  `decide_func` text NOT NULL,
  `skill_type` tinyint(4) NOT NULL,
  `parent_skill` int(11) NOT NULL DEFAULT -1,
  `special_int` int(11) DEFAULT -1,
  `obj_display` varchar(80) DEFAULT NULL,
  `req_save` tinyint(4) DEFAULT -1,
  `cooldown_num` smallint(5) unsigned DEFAULT 0,
  `cooldown_size` smallint(5) unsigned DEFAULT 0,
  `ability_calc_func` text DEFAULT NULL,
  `description` varchar(1080) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent_skill` (`parent_skill`),
  CONSTRAINT `skills_ibfk_1` FOREIGN KEY (`parent_skill`) REFERENCES `skills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1000344 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `skills_spell_flags`
--

DROP TABLE IF EXISTS `skills_spell_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skills_spell_flags` (
  `skill_id` int(11) NOT NULL,
  `flag_id` int(11) unsigned NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `skills_spell_flags_ibfk_1` (`skill_id`),
  KEY `flag_id` (`flag_id`),
  CONSTRAINT `skills_spell_flags_ibfk_1` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `skills_spell_flags_ibfk_2` FOREIGN KEY (`flag_id`) REFERENCES `spell_flags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1434 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `spell_flags`
--

DROP TABLE IF EXISTS `spell_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `spell_flags` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temp_skill_id_map`
--

DROP TABLE IF EXISTS `temp_skill_id_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_skill_id_map` (
  `old_id` int(11) DEFAULT NULL,
  `new_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `titles`
--

DROP TABLE IF EXISTS `titles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `titles` (
  `title_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `male_text` varchar(100) NOT NULL,
  `female_text` varchar(100) NOT NULL,
  `prepend` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`title_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed
