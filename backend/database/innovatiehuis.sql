-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.6.5-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for innovatieplatform
DROP DATABASE IF EXISTS `innovatieplatform`;
CREATE DATABASE IF NOT EXISTS `innovatieplatform` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `innovatieplatform`;

-- Dumping structure for table innovatieplatform.announcements
DROP TABLE IF EXISTS `announcements`;
CREATE TABLE IF NOT EXISTS `announcements` (
  `announcementid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `projectid` int(11) DEFAULT NULL,
  `content` text NOT NULL,
  `title` tinytext NOT NULL DEFAULT 'title',
  `timestamp` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`announcementid`),
  KEY `projectid_announcements` (`projectid`),
  KEY `userid2_announcements` (`userid`),
  CONSTRAINT `projectid_announcements` FOREIGN KEY (`projectid`) REFERENCES `projects` (`projectid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `userid2_announcements` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.announcements: ~9 rows (approximately)
DELETE FROM `announcements`;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` (`announcementid`, `userid`, `projectid`, `content`, `title`, `timestamp`) VALUES
	(1, 5, NULL, 'Hallo iedereen, vergeten jullie niet kerst met ons te vieren?\r\nGroeten de politie.', 'Kerst bij de Politie!', '2021-12-02 17:01:59'),
	(2, 5, NULL, 'Hoe verwijder ik Announcements? Dat zou toch een feature zijn?', 'Bug report', '2021-12-03 17:01:59'),
	(3, 5, 10, 'Haha mooi systeempje hoor jongens, lekker secure. :)', 'Lekker bezig', '2021-12-01 11:01:59'),
	(4, 6, 10, 'muhahahahha ik heb mezelf admin privileges gegeven', 'title', '1995-03-07 17:01:59'),
	(25, 5, NULL, 'line break\n\nline break', 'gggd', '2021-12-06 20:39:50'),
	(27, 5, NULL, '"<script>alert("HAHAHAHA");</script>"', '"<script>alert("HAHAHAHA");</script>"', '2021-12-07 14:09:23'),
	(52, 5, 10, 'Ik kan niets zien :(', 'Jongens het is donker', '2021-12-09 00:11:02'),
	(53, 5, 15, 'fdbfdbdf', 'fgdf', '2021-12-09 00:27:15'),
	(55, 5, 15, 'Ker-chunk', 'Pief poef pauw', '2021-12-09 00:43:26');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;

-- Dumping structure for table innovatieplatform.chat_messages
DROP TABLE IF EXISTS `chat_messages`;
CREATE TABLE IF NOT EXISTS `chat_messages` (
  `messageid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `projectid` int(11) NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp(),
  `content` text NOT NULL,
  PRIMARY KEY (`messageid`) USING BTREE,
  KEY `projectid_chat` (`projectid`),
  KEY `userid_chat` (`userid`),
  CONSTRAINT `projectid_chat` FOREIGN KEY (`projectid`) REFERENCES `projects` (`projectid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `userid_chat` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.chat_messages: ~7 rows (approximately)
DELETE FROM `chat_messages`;
/*!40000 ALTER TABLE `chat_messages` DISABLE KEYS */;
INSERT INTO `chat_messages` (`messageid`, `userid`, `projectid`, `timestamp`, `content`) VALUES
	(1, 1, 10, '2021-11-30 18:00:23', 'peter gaan we portal 2 doen?'),
	(2, 1, 10, '2021-11-30 18:00:23', 'peter gaan we portal 2 doen?'),
	(3, 1, 10, '2021-11-30 18:00:23', 'peter gaan we portal 2 doen?'),
	(4, 1, 10, '2021-11-30 18:00:23', 'peter gaan we portal 2 doen?'),
	(5, 2, 10, '2021-11-30 18:01:41', 'nadat het project af is'),
	(6, 2, 10, '2021-11-30 18:01:41', 'hond'),
	(7, 3, 10, '2021-11-30 18:02:31', 'ik wil wel portal 2 met je spelen hayo');
/*!40000 ALTER TABLE `chat_messages` ENABLE KEYS */;

-- Dumping structure for table innovatieplatform.projects
DROP TABLE IF EXISTS `projects`;
CREATE TABLE IF NOT EXISTS `projects` (
  `projectid` int(11) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(50) NOT NULL,
  `is_archived` tinyint(1) NOT NULL DEFAULT 0,
  `created` datetime NOT NULL DEFAULT current_timestamp(),
  `last_updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `description` text NOT NULL DEFAULT '',
  PRIMARY KEY (`projectid`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.projects: ~14 rows (approximately)
DELETE FROM `projects`;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` (`projectid`, `project_name`, `is_archived`, `created`, `last_updated`, `description`) VALUES
	(1, 'Project X', 0, '2021-11-30 18:27:30', '2021-12-09 14:07:01', ''),
	(2, 'Project X 2.0', 1, '2021-11-17 15:28:55', '2021-12-09 14:06:54', ''),
	(4, 'Brievenbusdrone', 0, '2021-11-17 15:32:44', '2021-11-30 17:52:30', ''),
	(5, 'Rattenval met 5G', 0, '2021-11-17 15:32:46', '2021-11-30 17:53:22', ''),
	(6, 'Talking Crime Scenes', 0, '2021-11-17 15:32:50', '2021-11-30 17:54:50', ''),
	(7, 'Slim Vest', 0, '2021-11-17 15:32:52', '2021-11-30 17:55:17', ''),
	(8, 'Briljant Vest', 0, '2021-11-30 18:28:23', '2021-11-30 18:28:23', ''),
	(9, 'Slimme Muts', 0, '2021-11-30 18:28:42', '2021-11-30 18:28:42', ''),
	(10, 'Intranet Platform', 0, '2021-11-17 17:02:08', '2021-11-30 19:14:26', ''),
	(11, 'Diplomaregister', 0, '2021-11-17 15:32:52', '2021-11-30 17:55:33', ''),
	(12, 'Sociale Robot', 1, '2021-11-17 15:32:52', '2021-11-30 17:55:39', ''),
	(13, 'Briljante Muts', 0, '2021-11-30 18:29:00', '2021-11-30 18:29:00', ''),
	(14, 'Intranet Git', 0, '2021-11-30 18:30:13', '2021-11-30 18:30:14', ''),
	(15, 'AR Schietbaan', 0, '2021-11-25 12:47:44', '2021-11-30 17:55:45', '');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;

-- Dumping structure for table innovatieplatform.projects_have_parents
DROP TABLE IF EXISTS `projects_have_parents`;
CREATE TABLE IF NOT EXISTS `projects_have_parents` (
  `parentid` int(11) NOT NULL,
  `childid` int(11) NOT NULL,
  `shared_files` text DEFAULT NULL,
  KEY `parentid` (`parentid`),
  KEY `childid` (`childid`),
  CONSTRAINT `childid` FOREIGN KEY (`childid`) REFERENCES `projects` (`projectid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `parentid` FOREIGN KEY (`parentid`) REFERENCES `projects` (`projectid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.projects_have_parents: ~6 rows (approximately)
DELETE FROM `projects_have_parents`;
/*!40000 ALTER TABLE `projects_have_parents` DISABLE KEYS */;
INSERT INTO `projects_have_parents` (`parentid`, `childid`, `shared_files`) VALUES
	(7, 8, NULL),
	(7, 9, NULL),
	(9, 13, NULL),
	(1, 2, NULL),
	(6, 12, NULL),
	(10, 14, 'file.txt folder/file.txt');
/*!40000 ALTER TABLE `projects_have_parents` ENABLE KEYS */;

-- Dumping structure for table innovatieplatform.replies
DROP TABLE IF EXISTS `replies`;
CREATE TABLE IF NOT EXISTS `replies` (
  `replyid` int(11) NOT NULL AUTO_INCREMENT,
  `announcementid` int(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `content` text NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`replyid`) USING BTREE,
  KEY `userid_announcement_replies` (`userid`),
  KEY `announcementid_announcement_replies` (`announcementid`),
  CONSTRAINT `announcementid_announcement_replies` FOREIGN KEY (`announcementid`) REFERENCES `announcements` (`announcementid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `userid_announcement_replies` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.replies: ~7 rows (approximately)
DELETE FROM `replies`;
/*!40000 ALTER TABLE `replies` DISABLE KEYS */;
INSERT INTO `replies` (`replyid`, `announcementid`, `userid`, `content`, `timestamp`) VALUES
	(1, 4, 5, 'hallo\n\nmiauw', '2021-11-30 18:22:43'),
	(2, 4, 1, 'hallo\n\nmiauw', '2021-11-30 18:22:59'),
	(4, 4, 1, 'hallo\n\nmiauw', '2021-12-06 22:42:54'),
	(5, 25, 1, 'hoera line breaks werken, maar niet hier blijkbaar', '2021-12-07 14:02:27'),
	(7, 25, 1, 'jweouwvwd\n\niwrivobdwds', '2021-12-08 15:14:31'),
	(15, 27, 1, 'hhhhaaaaddddddd', '2021-12-09 00:01:18'),
	(16, 1, 1, 'Moeten we kadootjes kopen?', '2021-12-09 15:19:18');
/*!40000 ALTER TABLE `replies` ENABLE KEYS */;

-- Dumping structure for table innovatieplatform.roles
DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `roleid` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) NOT NULL,
  `may_create_projects` tinyint(1) NOT NULL DEFAULT 0,
  `may_read_all_projects` tinyint(1) NOT NULL DEFAULT 0,
  `may_read_assigned_projects` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_all_projects` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_assigned_projects` tinyint(1) NOT NULL DEFAULT 0,
  `may_delete_all_projects` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_all_files` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_files_in_assigned_projects` tinyint(1) NOT NULL DEFAULT 0,
  `may_create_announcements_everywhere` tinyint(1) NOT NULL DEFAULT 0,
  `may_create_announcements_in_assigned_projects` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_all_announcements` tinyint(1) NOT NULL DEFAULT 0,
  `may_create_replies_everywhere` tinyint(1) NOT NULL DEFAULT 0,
  `may_create_replies_in_assigned_projects` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_all_replies` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_own_content` tinyint(1) NOT NULL DEFAULT 0,
  `may_read_all_users` tinyint(1) NOT NULL DEFAULT 0,
  `may_read_users_in_assigned_projects` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_all_user_passwords` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_own_password` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_all_user_details` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_own_details` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_all_user_roles` tinyint(1) NOT NULL DEFAULT 0,
  `may_crud_roles` tinyint(1) NOT NULL DEFAULT 0,
  `may_create_chat_messages_everywhere` tinyint(1) NOT NULL DEFAULT 0,
  `may_create_chat_messages_in_assigned_projects` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_chat_messages` tinyint(1) NOT NULL DEFAULT 0,
  `may_update_own_chat_messages` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`roleid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.roles: ~4 rows (approximately)
DELETE FROM `roles`;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` (`roleid`, `role_name`, `may_create_projects`, `may_read_all_projects`, `may_read_assigned_projects`, `may_update_all_projects`, `may_update_assigned_projects`, `may_delete_all_projects`, `may_update_all_files`, `may_update_files_in_assigned_projects`, `may_create_announcements_everywhere`, `may_create_announcements_in_assigned_projects`, `may_update_all_announcements`, `may_create_replies_everywhere`, `may_create_replies_in_assigned_projects`, `may_update_all_replies`, `may_update_own_content`, `may_read_all_users`, `may_read_users_in_assigned_projects`, `may_update_all_user_passwords`, `may_update_own_password`, `may_update_all_user_details`, `may_update_own_details`, `may_update_all_user_roles`, `may_crud_roles`, `may_create_chat_messages_everywhere`, `may_create_chat_messages_in_assigned_projects`, `may_update_chat_messages`, `may_update_own_chat_messages`) VALUES
	(1, 'observer', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(2, 'student', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(3, 'moderator', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	(4, 'admin', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;

-- Dumping structure for table innovatieplatform.users
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(40) NOT NULL,
  `last_name` varchar(40) NOT NULL,
  `email` tinytext NOT NULL,
  `password_hash` tinytext NOT NULL,
  `roleid` int(11) NOT NULL DEFAULT 0,
  `screening_status` tinyint(1) NOT NULL DEFAULT 0,
  `created` datetime NOT NULL DEFAULT current_timestamp(),
  `last_login` datetime DEFAULT current_timestamp(),
  `last_failed_login` datetime DEFAULT NULL,
  `failed_login_count` tinyint(4) NOT NULL DEFAULT 0,
  `last_timeout_started` datetime DEFAULT NULL,
  PRIMARY KEY (`userid`),
  KEY `role` (`roleid`),
  CONSTRAINT `role` FOREIGN KEY (`roleid`) REFERENCES `roles` (`roleid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.users: ~8 rows (approximately)
DELETE FROM `users`;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`userid`, `first_name`, `last_name`, `email`, `password_hash`, `roleid`, `screening_status`, `created`, `last_login`, `last_failed_login`, `failed_login_count`, `last_timeout_started`) VALUES
	(1, 'Hayo', 'Riem', 'hayoriem@mail.com', '123', 1, 0, '2021-11-30 17:47:09', '2021-11-30 17:47:09', NULL, 0, NULL),
	(2, 'Peter', 'Beens', 'peterbeens@mail.com', '123', 2, 0, '2021-11-30 17:47:41', '2021-11-30 17:47:41', NULL, 0, NULL),
	(3, 'Singh', 'van Offeren', 'singhvano@mail.com', '123', 2, 0, '2021-11-30 17:48:24', '2021-11-30 17:48:24', NULL, 0, NULL),
	(4, 'Jochem', 'Hoekstra', 'joja@mail.com', '123', 2, 0, '2021-11-30 17:48:47', '2021-11-30 17:48:47', NULL, 0, NULL),
	(5, 'Niels', 'Doornbos', 'nielsprikkelbos@mail.com', '123', 4, 0, '2021-11-30 17:49:09', '2021-11-30 17:49:09', NULL, 0, NULL),
	(6, 'Jan', 'Baljé', 'janbal@mail.com', '123', 1, 0, '2021-11-30 17:49:49', '2021-11-30 17:49:49', NULL, 0, NULL),
	(7, 'Tim', 'Dronebos', 'tim@mail.com', '123', 3, 0, '2021-11-30 17:51:50', '2021-11-30 17:51:50', NULL, 0, NULL),
	(8, 'pieter', 'van rosmalen', 'pvr@mail.com', '123458', 3, 0, '2021-12-02 19:09:21', '2021-12-02 19:09:21', NULL, 0, NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

-- Dumping structure for table innovatieplatform.users_have_projects
DROP TABLE IF EXISTS `users_have_projects`;
CREATE TABLE IF NOT EXISTS `users_have_projects` (
  `userid` int(11) NOT NULL,
  `projectid` int(11) NOT NULL,
  `last_seen` datetime NOT NULL DEFAULT current_timestamp(),
  KEY `userid_user_has_projects` (`userid`),
  KEY `projectid_user_has_projects` (`projectid`),
  CONSTRAINT `projectid_user_has_projects` FOREIGN KEY (`projectid`) REFERENCES `projects` (`projectid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `userid_user_has_projects` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.users_have_projects: ~15 rows (approximately)
DELETE FROM `users_have_projects`;
/*!40000 ALTER TABLE `users_have_projects` DISABLE KEYS */;
INSERT INTO `users_have_projects` (`userid`, `projectid`, `last_seen`) VALUES
	(1, 10, '2021-11-30 17:57:20'),
	(4, 10, '2021-11-30 17:57:30'),
	(3, 10, '2021-11-30 17:57:41'),
	(2, 10, '2021-11-30 17:57:49'),
	(5, 10, '2021-11-30 17:57:58'),
	(7, 10, '2021-11-30 17:58:22'),
	(6, 10, '2021-11-30 17:58:29'),
	(7, 4, '2021-11-30 17:58:44'),
	(7, 2, '2021-11-30 17:58:54'),
	(7, 5, '2021-11-30 17:58:54'),
	(7, 7, '2021-11-30 17:58:54'),
	(7, 15, '2021-11-30 17:58:54'),
	(7, 11, '2021-11-30 17:58:54'),
	(5, 15, '2021-11-30 17:58:54'),
	(1, 15, '2021-12-09 00:06:46');
/*!40000 ALTER TABLE `users_have_projects` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
