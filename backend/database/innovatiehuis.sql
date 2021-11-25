-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server versie:                10.6.5-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Versie:              11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Databasestructuur van innovatieplatform wordt geschreven
DROP DATABASE IF EXISTS `innovatieplatform`;
CREATE DATABASE IF NOT EXISTS `innovatieplatform` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `innovatieplatform`;

-- Structuur van  tabel innovatieplatform.announcements wordt geschreven
DROP TABLE IF EXISTS `announcements`;
CREATE TABLE IF NOT EXISTS `announcements` (
  `announcementid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `projectid` int(11) DEFAULT NULL,
  `contents` text NOT NULL,
  PRIMARY KEY (`announcementid`),
  KEY `projectid_announcements` (`projectid`),
  KEY `userid2_announcements` (`userid`),
  CONSTRAINT `projectid_announcements` FOREIGN KEY (`projectid`) REFERENCES `projects` (`projectid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `userid2_announcements` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumpen data van tabel innovatieplatform.announcements: ~0 rows (ongeveer)
DELETE FROM `announcements`;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;

-- Structuur van  tabel innovatieplatform.announcement_replies wordt geschreven
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumpen data van tabel innovatieplatform.announcement_replies: ~0 rows (ongeveer)
DELETE FROM `announcement_replies`;
/*!40000 ALTER TABLE `announcement_replies` DISABLE KEYS */;
/*!40000 ALTER TABLE `announcement_replies` ENABLE KEYS */;

-- Structuur van  tabel innovatieplatform.chat_messages wordt geschreven
DROP TABLE IF EXISTS `chat_messages`;
CREATE TABLE IF NOT EXISTS `chat_messages` (
  `meesageid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `projectid` int(11) NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp(),
  `content` text NOT NULL,
  PRIMARY KEY (`meesageid`),
  KEY `projectid_chat` (`projectid`),
  KEY `userid_chat` (`userid`),
  CONSTRAINT `projectid_chat` FOREIGN KEY (`projectid`) REFERENCES `projects` (`projectid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `userid_chat` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumpen data van tabel innovatieplatform.chat_messages: ~0 rows (ongeveer)
DELETE FROM `chat_messages`;
/*!40000 ALTER TABLE `chat_messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_messages` ENABLE KEYS */;

-- Structuur van  tabel innovatieplatform.projects wordt geschreven
DROP TABLE IF EXISTS `projects`;
CREATE TABLE IF NOT EXISTS `projects` (
  `projectid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `isarchived` tinyint(1) NOT NULL DEFAULT 0,
  `createdat` datetime NOT NULL DEFAULT current_timestamp(),
  `lastupdated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`projectid`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

-- Dumpen data van tabel innovatieplatform.projects: ~9 rows (ongeveer)
DELETE FROM `projects`;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` (`projectid`, `name`, `isarchived`, `createdat`, `lastupdated`) VALUES
	(2, 'Project X 2.0', 1, '2021-11-17 15:28:55', '2021-11-18 14:20:43'),
	(4, 'Project1', 0, '2021-11-17 15:32:44', '2021-11-17 17:40:44'),
	(5, 'Project2', 0, '2021-11-17 15:32:46', '2021-11-17 17:40:46'),
	(6, 'Project3', 0, '2021-11-17 15:32:50', '2021-11-17 17:41:00'),
	(7, 'Project4', 0, '2021-11-17 15:32:52', '2021-11-17 17:40:20'),
	(10, 'Intranet', 0, '2021-11-17 17:02:08', '2021-11-17 17:45:48'),
	(11, 'Project5', 0, '2021-11-17 15:32:52', '2021-11-17 17:41:05'),
	(12, 'Project6', 1, '2021-11-17 15:32:52', '2021-11-17 17:46:06'),
	(15, 'hond', 0, '2021-11-25 12:47:44', '2021-11-25 12:47:44');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;

-- Structuur van  tabel innovatieplatform.projects_has_parents wordt geschreven
DROP TABLE IF EXISTS `projects_has_parents`;
CREATE TABLE IF NOT EXISTS `projects_has_parents` (
  `parentid` int(11) NOT NULL,
  `childid` int(11) NOT NULL,
  KEY `parentid` (`parentid`),
  KEY `childid` (`childid`),
  CONSTRAINT `childid` FOREIGN KEY (`childid`) REFERENCES `projects` (`projectid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `parentid` FOREIGN KEY (`parentid`) REFERENCES `projects` (`projectid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumpen data van tabel innovatieplatform.projects_has_parents: ~0 rows (ongeveer)
DELETE FROM `projects_has_parents`;
/*!40000 ALTER TABLE `projects_has_parents` DISABLE KEYS */;
/*!40000 ALTER TABLE `projects_has_parents` ENABLE KEYS */;

-- Structuur van  tabel innovatieplatform.roles wordt geschreven
DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `roleid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT 'observer',
  `crud_files_in_own_project` tinyint(1) NOT NULL DEFAULT 0,
  `edit_own_project` tinyint(1) NOT NULL DEFAULT 0,
  `see_all_projects` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`roleid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumpen data van tabel innovatieplatform.roles: ~0 rows (ongeveer)
DELETE FROM `roles`;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;

-- Structuur van  tabel innovatieplatform.users wordt geschreven
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
  `lastwrongpassword` datetime NOT NULL,
  `wrongpasswordcount` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`userid`),
  KEY `role` (`roleid`),
  CONSTRAINT `role` FOREIGN KEY (`roleid`) REFERENCES `roles` (`roleid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumpen data van tabel innovatieplatform.users: ~0 rows (ongeveer)
DELETE FROM `users`;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

-- Structuur van  tabel innovatieplatform.user_has_projects wordt geschreven
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

-- Dumpen data van tabel innovatieplatform.user_has_projects: ~0 rows (ongeveer)
DELETE FROM `user_has_projects`;
/*!40000 ALTER TABLE `user_has_projects` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_has_projects` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
