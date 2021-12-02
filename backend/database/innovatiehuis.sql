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
  PRIMARY KEY (`announcementid`),
  KEY `projectid_announcements` (`projectid`),
  KEY `userid2_announcements` (`userid`),
  CONSTRAINT `projectid_announcements` FOREIGN KEY (`projectid`) REFERENCES `projects` (`projectid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `userid2_announcements` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.announcements: ~4 rows (approximately)
DELETE FROM `announcements`;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` (`announcementid`, `userid`, `projectid`, `content`, `title`) VALUES
	(1, 5, NULL, 'Hallo iedereen, vergeten jullie niet kerst met ons te vieren?\r\nGroeten de politie.', 'Kerst bij de Politie!'),
	(2, 5, NULL, 'Hoe verwijder ik Announcements? Dat zou toch een feature zijn?', 'Bug report'),
	(3, 5, 10, 'Haha mooi systeempje hoor jongens, lekker secure. :)', 'Lekker bezig'),
	(4, 6, 10, 'muhahahahha ik heb mezelf admin privileges gegeven', 'title');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;

-- Dumping structure for table innovatieplatform.announcement_replies
DROP TABLE IF EXISTS `announcement_replies`;
CREATE TABLE IF NOT EXISTS `announcement_replies` (
  `announcement_replies_id` int(11) NOT NULL AUTO_INCREMENT,
  `announcementid` int(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `content` text NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`announcement_replies_id`) USING BTREE,
  KEY `userid_announcement_replies` (`userid`),
  KEY `announcementid_announcement_replies` (`announcementid`),
  CONSTRAINT `announcementid_announcement_replies` FOREIGN KEY (`announcementid`) REFERENCES `announcements` (`announcementid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `userid_announcement_replies` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.announcement_replies: ~2 rows (approximately)
DELETE FROM `announcement_replies`;
/*!40000 ALTER TABLE `announcement_replies` DISABLE KEYS */;
INSERT INTO `announcement_replies` (`announcement_replies_id`, `announcementid`, `userid`, `content`, `timestamp`) VALUES
	(1, 4, 5, 'Neee niet mijn platformpie :^(', '2021-11-30 18:22:43'),
	(2, 4, 1, 'Boe gemene man, ga weg', '2021-11-30 18:22:59');
/*!40000 ALTER TABLE `announcement_replies` ENABLE KEYS */;

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
  `name` varchar(50) NOT NULL,
  `isarchived` tinyint(1) NOT NULL DEFAULT 0,
  `createdat` datetime NOT NULL DEFAULT current_timestamp(),
  `lastupdated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`projectid`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.projects: ~14 rows (approximately)
DELETE FROM `projects`;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` (`projectid`, `name`, `isarchived`, `createdat`, `lastupdated`) VALUES
	(1, 'Project X', 1, '2021-11-30 18:27:30', '2021-11-30 18:27:39'),
	(2, 'Project X 2.0', 0, '2021-11-17 15:28:55', '2021-11-30 18:27:33'),
	(4, 'Brievenbusdrone', 0, '2021-11-17 15:32:44', '2021-11-30 17:52:30'),
	(5, 'Rattenval met 5G', 0, '2021-11-17 15:32:46', '2021-11-30 17:53:22'),
	(6, 'Talking Crime Scenes', 0, '2021-11-17 15:32:50', '2021-11-30 17:54:50'),
	(7, 'Slim Vest', 0, '2021-11-17 15:32:52', '2021-11-30 17:55:17'),
	(8, 'Briljant Vest', 0, '2021-11-30 18:28:23', '2021-11-30 18:28:23'),
	(9, 'Slimme Muts', 0, '2021-11-30 18:28:42', '2021-11-30 18:28:42'),
	(10, 'Intranet Platform', 0, '2021-11-17 17:02:08', '2021-11-30 19:14:26'),
	(11, 'Diplomaregister', 0, '2021-11-17 15:32:52', '2021-11-30 17:55:33'),
	(12, 'Sociale Robot', 1, '2021-11-17 15:32:52', '2021-11-30 17:55:39'),
	(13, 'Briljante Muts', 0, '2021-11-30 18:29:00', '2021-11-30 18:29:00'),
	(14, 'Intranet Git', 0, '2021-11-30 18:30:13', '2021-11-30 18:30:14'),
	(15, 'AR Schietbaan', 0, '2021-11-25 12:47:44', '2021-11-30 17:55:45');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;

-- Dumping structure for table innovatieplatform.projects_has_parents
DROP TABLE IF EXISTS `projects_has_parents`;
CREATE TABLE IF NOT EXISTS `projects_has_parents` (
  `parentid` int(11) NOT NULL,
  `childid` int(11) NOT NULL,
  `shared_files` text DEFAULT NULL,
  KEY `parentid` (`parentid`),
  KEY `childid` (`childid`),
  CONSTRAINT `childid` FOREIGN KEY (`childid`) REFERENCES `projects` (`projectid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `parentid` FOREIGN KEY (`parentid`) REFERENCES `projects` (`projectid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.projects_has_parents: ~6 rows (approximately)
DELETE FROM `projects_has_parents`;
/*!40000 ALTER TABLE `projects_has_parents` DISABLE KEYS */;
INSERT INTO `projects_has_parents` (`parentid`, `childid`, `shared_files`) VALUES
	(7, 8, NULL),
	(7, 9, NULL),
	(9, 13, NULL),
	(1, 2, NULL),
	(6, 12, NULL),
	(10, 14, 'file.txt folder/file.txt');
/*!40000 ALTER TABLE `projects_has_parents` ENABLE KEYS */;

-- Dumping structure for table innovatieplatform.roles
DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `roleid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `crud_files_in_own_project` tinyint(1) NOT NULL DEFAULT 0,
  `edit_own_project` tinyint(1) NOT NULL DEFAULT 0,
  `edit_permissions` tinyint(1) NOT NULL DEFAULT 0,
  `see_all_projects` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`roleid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.roles: ~4 rows (approximately)
DELETE FROM `roles`;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` (`roleid`, `name`, `crud_files_in_own_project`, `edit_own_project`, `edit_permissions`, `see_all_projects`) VALUES
	(1, 'observer', 0, 0, 0, 0),
	(2, 'student', 0, 0, 0, 0),
	(3, 'moderator', 0, 0, 0, 0),
	(4, 'admin', 0, 0, 0, 0);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;

-- Dumping structure for table innovatieplatform.users
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(40) NOT NULL,
  `lastname` varchar(40) NOT NULL,
  `email` tinytext NOT NULL,
  `password` tinytext NOT NULL,
  `roleid` int(11) NOT NULL DEFAULT 0,
  `statusvog` tinyint(1) NOT NULL DEFAULT 0,
  `statusgeheimhouding` tinyint(1) NOT NULL DEFAULT 0,
  `createdat` datetime NOT NULL DEFAULT current_timestamp(),
  `lastwrongpassword` datetime NOT NULL DEFAULT current_timestamp(),
  `wrongpasswordcount` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`userid`),
  KEY `role` (`roleid`),
  CONSTRAINT `role` FOREIGN KEY (`roleid`) REFERENCES `roles` (`roleid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.users: ~7 rows (approximately)
DELETE FROM `users`;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`userid`, `firstname`, `lastname`, `email`, `password`, `roleid`, `statusvog`, `statusgeheimhouding`, `createdat`, `lastwrongpassword`, `wrongpasswordcount`) VALUES
	(1, 'Hayo', 'Riem', 'hayoriem@mail.com', '123', 1, 0, 0, '2021-11-30 17:47:09', '2021-11-30 17:47:09', 0),
	(2, 'Peter', 'Beens', 'peterbeens@mail.com', '123', 2, 0, 0, '2021-11-30 17:47:41', '2021-11-30 17:47:41', 0),
	(3, 'Singh', 'van Offeren', 'singhvano@mail.com', '123', 2, 0, 0, '2021-11-30 17:48:24', '2021-11-30 17:48:24', 0),
	(4, 'Jochem', 'Hoekstra', 'joja@mail.com', '123', 2, 0, 0, '2021-11-30 17:48:47', '2021-11-30 17:48:47', 0),
	(5, 'Niels', 'Doornbos', 'nielsprikkelbos@mail.com', '123', 4, 0, 0, '2021-11-30 17:49:09', '2021-11-30 17:49:09', 0),
	(6, 'Jan', 'Baljé', 'janbal@mail.com', '123', 1, 0, 0, '2021-11-30 17:49:49', '2021-11-30 17:49:49', 0),
	(7, 'Tim', 'Dronebos', 'tim@mail.com', '123', 3, 0, 0, '2021-11-30 17:51:50', '2021-11-30 17:51:50', 0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

-- Dumping structure for table innovatieplatform.user_has_projects
DROP TABLE IF EXISTS `user_has_projects`;
CREATE TABLE IF NOT EXISTS `user_has_projects` (
  `userid` int(11) NOT NULL,
  `projectid` int(11) NOT NULL,
  `lastseen` datetime NOT NULL DEFAULT current_timestamp(),
  KEY `userid_user_has_projects` (`userid`),
  KEY `projectid_user_has_projects` (`projectid`),
  CONSTRAINT `projectid_user_has_projects` FOREIGN KEY (`projectid`) REFERENCES `projects` (`projectid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `userid_user_has_projects` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table innovatieplatform.user_has_projects: ~14 rows (approximately)
DELETE FROM `user_has_projects`;
/*!40000 ALTER TABLE `user_has_projects` DISABLE KEYS */;
INSERT INTO `user_has_projects` (`userid`, `projectid`, `lastseen`) VALUES
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
	(5, 15, '2021-11-30 17:58:54');
/*!40000 ALTER TABLE `user_has_projects` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
