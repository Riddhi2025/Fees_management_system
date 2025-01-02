/*
SQLyog Enterprise - MySQL GUI v8.02 RC
MySQL - 5.5.5-10.4.17-MariaDB : Database - student_fee
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`student_fee` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `student_fee`;

/*Table structure for table `accountant` */

DROP TABLE IF EXISTS `accountant`;

CREATE TABLE `accountant` (
  `emp_no` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `designation` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `accountant` */

insert  into `accountant`(`emp_no`,`name`,`designation`,`contact`,`email`) values ('A1001','Punit sharma','Accountant','9529676199','p@gmail.com');

/*Table structure for table `admin_data` */

DROP TABLE IF EXISTS `admin_data`;

CREATE TABLE `admin_data` (
  `name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `admin_data` */

insert  into `admin_data`(`name`,`address`,`contact`,`email`) values ('Abhishek Sharma','Rangbari Kota','9529676198','a@gmail.com');

/*Table structure for table `course_master` */

DROP TABLE IF EXISTS `course_master`;

CREATE TABLE `course_master` (
  `course` varchar(100) NOT NULL,
  `fee` int(11) DEFAULT NULL,
  `duration` varchar(100) DEFAULT NULL,
  `remarks` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`course`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `course_master` */

insert  into `course_master`(`course`,`fee`,`duration`,`remarks`) values ('C Programming',4500,'Two Months','Basic Programing lanuage'),('CPP',4500,'Two Months','Advanse version of c with OOPs concepts'),('DSA',4000,'Two Months','Data structure & Algorithms for logic  building '),('JAVA',8000,' Three Months','JAVA is a object oriented programming lanuage'),('PYTHON',8000,'FOUR MONTHS','Pyhton is lanuage used to deal with data base /Dynamic language'),('SOFTWARE DEVELOPMENT',60000,'Eight months','In this course we used to create Software'),('Web Designing',15000,' Three Months','HTML,CSS,JAVASCRIPT,JQUERY,MEADIAQUERY');

/*Table structure for table `login_data` */

DROP TABLE IF EXISTS `login_data`;

CREATE TABLE `login_data` (
  `email` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `con_pass` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `login_data` */

insert  into `login_data`(`email`,`password`,`con_pass`,`usertype`) values ('a@gmail.com','aa','aa','admin'),('p@gmail.com','pp','pp','accountant');

/*Table structure for table `photodata` */

DROP TABLE IF EXISTS `photodata`;

CREATE TABLE `photodata` (
  `user_email` varchar(100) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `photodata` */

insert  into `photodata`(`user_email`,`photo`) values ('a@gmail.com','1715673057.jpg'),('p@gmail.com','1715840750.jpg');

/*Table structure for table `st_course` */

DROP TABLE IF EXISTS `st_course`;

CREATE TABLE `st_course` (
  `course_id` int(11) NOT NULL AUTO_INCREMENT,
  `reg_no` int(11) DEFAULT NULL,
  `course` varchar(100) DEFAULT NULL,
  `fee` int(11) DEFAULT NULL,
  `discount` int(11) DEFAULT NULL,
  `join_date` date DEFAULT NULL,
  `remarks` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

/*Data for the table `st_course` */

insert  into `st_course`(`course_id`,`reg_no`,`course`,`fee`,`discount`,`join_date`,`remarks`) values (1,19,'C Programing',4500,1000,'2024-04-12','Basic programming language'),(2,19,'CPP',4000,500,'2024-04-12','STL with CPP'),(3,20,'JAVA',8000,1000,'2024-04-13','refrence by vansh jaat'),(4,20,'C Programming',4500,500,'2024-04-13','Refrence by punit sharma'),(5,21,'Web Designing',15000,2000,'2024-04-14','second year student'),(6,22,'PYTHON',8000,1000,'2024-04-13','reference by abhishek'),(7,19,'Web Designing',15000,1000,'2024-05-20','tyu'),(8,23,'DSA',4500,500,'2024-04-14','student_course bt apex collage');

/*Table structure for table `st_data` */

DROP TABLE IF EXISTS `st_data`;

CREATE TABLE `st_data` (
  `reg_no` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`reg_no`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4;

/*Data for the table `st_data` */

insert  into `st_data`(`reg_no`,`name`,`address`,`contact`,`email`) values (19,'Ronak sharma','vivekanad nagar','8824058729','r@gmail.com'),(20,'Madhur Sharma','dadabari','800128447','m@gmail.com'),(21,'Abishek sharma','Rangbari','9529676199','a@gmail.com'),(22,'Ansh jain','kunadi','8507417852','a@'),(23,'Vansh Jaat','Dcm','855025854','v@gmail.com');

/*Table structure for table `st_fee` */

DROP TABLE IF EXISTS `st_fee`;

CREATE TABLE `st_fee` (
  `tno` int(11) NOT NULL AUTO_INCREMENT,
  `reg_no` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `deposit_date` date DEFAULT NULL,
  `remarks` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`tno`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

/*Data for the table `st_fee` */

insert  into `st_fee`(`tno`,`reg_no`,`course_id`,`amount`,`deposit_date`,`remarks`) values (1,19,1,2500,'2024-04-11','Remaining amount is 1000/-'),(2,19,2,2000,'2024-04-11','2000 yet to be deposited'),(3,20,3,4000,'2024-04-13','3000'),(4,20,4,2000,'2024-04-13','2000 remaining'),(5,21,5,5000,'2024-04-14','8000 remaining'),(6,22,6,4000,'2024-04-12','2000'),(7,23,8,4000,'2024-04-14','all amount are deposit'),(8,19,7,7000,'2024-05-20','7000k re');

/*Table structure for table `accountant_with_photo` */

DROP TABLE IF EXISTS `accountant_with_photo`;

/*!50001 DROP VIEW IF EXISTS `accountant_with_photo` */;
/*!50001 DROP TABLE IF EXISTS `accountant_with_photo` */;

/*!50001 CREATE TABLE `accountant_with_photo` (
  `emp_no` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `designation` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `photo` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 */;

/*Table structure for table `admin_with_photo` */

DROP TABLE IF EXISTS `admin_with_photo`;

/*!50001 DROP VIEW IF EXISTS `admin_with_photo` */;
/*!50001 DROP TABLE IF EXISTS `admin_with_photo` */;

/*!50001 CREATE TABLE `admin_with_photo` (
  `name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `photo` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 */;

/*Table structure for table `student_with_photo` */

DROP TABLE IF EXISTS `student_with_photo`;

/*!50001 DROP VIEW IF EXISTS `student_with_photo` */;
/*!50001 DROP TABLE IF EXISTS `student_with_photo` */;

/*!50001 CREATE TABLE `student_with_photo` (
  `reg_no` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `user_email` varchar(100) NOT NULL,
  `photo` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 */;

/*View structure for view accountant_with_photo */

/*!50001 DROP TABLE IF EXISTS `accountant_with_photo` */;
/*!50001 DROP VIEW IF EXISTS `accountant_with_photo` */;

/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `accountant_with_photo` AS (select `accountant`.`emp_no` AS `emp_no`,`accountant`.`name` AS `name`,`accountant`.`designation` AS `designation`,`accountant`.`contact` AS `contact`,`accountant`.`email` AS `email`,`photodata`.`user_email` AS `user_email`,`photodata`.`photo` AS `photo` from (`accountant` join `photodata` on(`accountant`.`email` = `photodata`.`user_email`))) */;

/*View structure for view admin_with_photo */

/*!50001 DROP TABLE IF EXISTS `admin_with_photo` */;
/*!50001 DROP VIEW IF EXISTS `admin_with_photo` */;

/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `admin_with_photo` AS (select `admin_data`.`name` AS `name`,`admin_data`.`address` AS `address`,`admin_data`.`contact` AS `contact`,`admin_data`.`email` AS `email`,`photodata`.`user_email` AS `user_email`,`photodata`.`photo` AS `photo` from (`admin_data` join `photodata` on(`admin_data`.`email` = `photodata`.`user_email`))) */;

/*View structure for view student_with_photo */

/*!50001 DROP TABLE IF EXISTS `student_with_photo` */;
/*!50001 DROP VIEW IF EXISTS `student_with_photo` */;

/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `student_with_photo` AS (select `st_data`.`reg_no` AS `reg_no`,`st_data`.`name` AS `name`,`st_data`.`address` AS `address`,`st_data`.`contact` AS `contact`,`st_data`.`email` AS `email`,`photodata`.`user_email` AS `user_email`,`photodata`.`photo` AS `photo` from (`st_data` join `photodata` on(`st_data`.`email` = `photodata`.`user_email`))) */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
