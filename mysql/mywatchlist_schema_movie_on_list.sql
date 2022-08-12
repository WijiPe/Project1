-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: mywatchlist_schema
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `movie_on_list`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `movie_on_list` (
  `id` int NOT NULL AUTO_INCREMENT,
  `director` varchar(115) DEFAULT NULL,
  `title` varchar(115) DEFAULT NULL,
  `movie_id` varchar(115) DEFAULT NULL,
  `watch_time` int NOT NULL DEFAULT '0',
  `movie_list_id` int NOT NULL,
  `top5movie` tinyint(1) NOT NULL,
  `poster_path` varchar(115) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_movie_on_list_movies_lists1_idx` (`movie_list_id`),
  CONSTRAINT `fk_movie_on_list_movies_lists1` FOREIGN KEY (`movie_list_id`) REFERENCES `movie_list` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie_on_list`
--

LOCK TABLES `movie_on_list` WRITE;
/*!40000 ALTER TABLE `movie_on_list` DISABLE KEYS */;
INSERT INTO `movie_on_list` VALUES (14,'ABC','Venom: Let There Be Carnage','580489',0,16,0,'/rjkmN1dniUHVYAtwuV3Tji7FsDO.jpg'),(15,'ABC','Spider-Man: No Way Home','634649',0,17,0,'/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg'),(16,'Coming Soon!','The Amazing Spider-Man 2','102382',2,18,0,'/c3e9e18SSlvFd1cQaGmUj5tqL5P.jpg'),(17,'Coming Soon!','Red Notice','512195',1,19,0,'/lAXONuqg41NwUMuzMiFvicDET9Y.jpg'),(18,'Coming Soon!','Shang-Chi and the Legend of the Ten Rings','566525',1,20,1,'/1BIoJGKbXjdFDAqUEiA2VHqkK1Z.jpg'),(19,'Coming Soon!','Spider-Man','557',1,21,1,'/gSZyYEK5AfZuOFFjnVPUCLvdOD6.jpg'),(20,'Coming Soon!','Spider-Man: Far From Home','429617',1,22,1,'/4q2NNj4S5dG2RLF9CpXsej7yXl.jpg'),(21,'ABC','Clifford the Big Red Dog','585245',0,23,0,'/ygPTrycbMSFDc5zUpy4K5ZZtQSC.jpg'),(22,'ABC','Eternals','524434',1,24,0,'/6AdXwFTRTAzggD2QUTt5B7JFGKL.jpg'),(23,'ABC','The Matrix Resurrections','624860',0,25,0,'/8c4a8kE7PizaGQQnditMmI1xbRp.jpg'),(24,'ABC','Free Guy','550988',0,26,0,'/xmbU4JTUm8rsdtn7Y3Fcm30GpeT.jpg'),(25,'Coming Soon!','Luca','508943',1,27,0,'/jTswp6KyDYKtvC52GbHagrZbGvD.jpg'),(26,'Coming Soon!','Captain America: Civil War','271110',1,28,1,'/rAGiXaUfPzY7CDEyNKUofk3Kw2e.jpg'),(27,'Coming Soon!','Harry Potter and the Half-Blood Prince','767',3,29,0,'/z7uo9zmQdQwU5ZJHFpv2Upl30i1.jpg'),(29,'Coming Soon!','Soul','508442',2,31,0,'/hm58Jw4Lw8OIeECIq5qyPYhAeRJ.jpg'),(31,'Coming Soon!','The Godfather','238',12,33,1,'/eEslKSwcqmiNS6va24Pbxf2UKmJ.jpg'),(32,'Coming Soon!','The Godfather: Part II','240',5,34,0,'/sSuQTCZwqKrNBNIsksO9IAUoWP9.jpg'),(33,'Coming Soon!','The Godfather: Part III','242',3,35,0,'/lm3pQ2QoQ16pextRsmnUbG2onES.jpg'),(44,'Hank Braxtan','Jurassic Hunt','848278',1,46,0,'/bZnOioDq1ldaxKfUoj3DenHU7mp.jpg'),(45,'Roger Kumble','After We Collided','613504',0,47,0,'/kiX7UYfOpYrMFSAGbI6j1pFkLzQ.jpg'),(46,'Domee Shi','Turning Red','508947',1,48,0,'/qsdjk9oAKSQMWs0Vt5Pyfh6O4GZ.jpg'),(47,'Shawn Levy','The Adam Project','696806',1,49,0,'/wFjboE0aFZNbVOF05fzrka9Fqyx.jpg'),(48,'Matt Reeves','The Batman','414906',1,50,0,'/74xTEgt7R36Fpooo50r9T25onhq.jpg'),(49,'Damien Power','No Exit','833425',1,51,0,'/5cnLoWq9o5tuLe1Zq4BTX4LwZ2B.jpg'),(50,'Anthony Hayes','Gold','760926',0,52,0,'/ejXBuNLvK4kZ7YcqeKqUWnCxdJq.jpg'),(51,'Rawson Marshall Thurber','Red Notice','512195',0,53,0,'/wdE6ewaKZHr62bLqCn7A2DiGShm.jpg'),(52,'Domee Shi','Turning Red','508947',0,54,0,'/qsdjk9oAKSQMWs0Vt5Pyfh6O4GZ.jpg');
/*!40000 ALTER TABLE `movie_on_list` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-07 11:39:51
