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

-- Dumpen data van tabel innovatieplatform.projects: ~10 rows (ongeveer)
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

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
