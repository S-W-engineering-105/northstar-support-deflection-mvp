/*
SQLyog Community v13.3.1 (64 bit)
MySQL - 10.4.32-MariaDB : Database - northstar_chatbot
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`northstar_chatbot` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `northstar_chatbot`;

/*Table structure for table `conversation_log` */

DROP TABLE IF EXISTS `conversation_log`;

CREATE TABLE `conversation_log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `session_id` varchar(50) NOT NULL,
  `intent` varchar(50) DEFAULT NULL,
  `query_type` enum('order_status','stock_check','greeting','out_of_scope','unclear') DEFAULT NULL,
  `was_successful` tinyint(1) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `conversation_log` */

/*Table structure for table `inventory` */

DROP TABLE IF EXISTS `inventory`;

CREATE TABLE `inventory` (
  `product_id` varchar(20) NOT NULL,
  `product_name` varchar(150) NOT NULL,
  `size` varchar(10) NOT NULL,
  `quantity_available` int(11) NOT NULL DEFAULT 0 CHECK (`quantity_available` >= 0),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `unique_product_size` (`product_name`,`size`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `inventory` */

insert  into `inventory`(`product_id`,`product_name`,`size`,`quantity_available`,`created_at`) values 
('PRD-001','Nike Air Force 1','40',5,'2026-08-15 12:25:03'),
('PRD-002','Nike Air Force 1','41',3,'2026-08-15 12:25:03'),
('PRD-003','Nike Air Force 1','42',7,'2026-08-15 12:25:03'),
('PRD-004','Nike Air Force 1','43',0,'2026-08-15 12:25:03'),
('PRD-005','Nike Air Force 1','44',2,'2026-08-15 12:25:03'),
('PRD-006','Adidas Ultraboost','40',4,'2026-08-15 12:25:03'),
('PRD-007','Adidas Ultraboost','41',6,'2026-08-15 12:25:03'),
('PRD-008','Adidas Ultraboost','42',0,'2026-08-15 12:25:03'),
('PRD-009','Adidas Ultraboost','43',3,'2026-08-15 12:25:03'),
('PRD-010','Adidas Ultraboost','44',1,'2026-08-15 12:25:03'),
('PRD-011','Puma RS-X','39',8,'2026-08-15 12:25:03'),
('PRD-012','Puma RS-X','40',5,'2026-08-15 12:25:03'),
('PRD-013','Puma RS-X','41',0,'2026-08-15 12:25:03'),
('PRD-014','Puma RS-X','42',4,'2026-08-15 12:25:03'),
('PRD-015','Puma RS-X','43',2,'2026-08-15 12:25:03'),
('PRD-016','New Balance 550','40',6,'2026-08-15 12:25:03'),
('PRD-017','New Balance 550','41',3,'2026-08-15 12:25:03'),
('PRD-018','New Balance 550','42',5,'2026-08-15 12:25:03'),
('PRD-019','New Balance 550','43',0,'2026-08-15 12:25:03'),
('PRD-020','New Balance 550','44',1,'2026-08-15 12:25:03'),
('PRD-021','Converse Chuck Taylor','38',10,'2026-08-15 12:25:03'),
('PRD-022','Converse Chuck Taylor','39',7,'2026-08-15 12:25:03'),
('PRD-023','Converse Chuck Taylor','40',4,'2026-08-15 12:25:03'),
('PRD-024','Converse Chuck Taylor','41',0,'2026-08-15 12:25:03'),
('PRD-025','Converse Chuck Taylor','42',6,'2026-08-15 12:25:03'),
('PRD-026','Vans Old Skool','39',5,'2026-08-15 12:25:03'),
('PRD-027','Vans Old Skool','40',3,'2026-08-15 12:25:03'),
('PRD-028','Vans Old Skool','41',8,'2026-08-15 12:25:03'),
('PRD-029','Vans Old Skool','42',0,'2026-08-15 12:25:03'),
('PRD-030','Vans Old Skool','43',2,'2026-08-15 12:25:03');

/*Table structure for table `orders` */

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `order_id` varchar(20) NOT NULL,
  `customer_name` varchar(100) NOT NULL,
  `status` enum('Processing','Shipped','Out for Delivery','Delivered') NOT NULL DEFAULT 'Processing',
  `order_date` date NOT NULL,
  `expected_delivery_date` date NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `orders` */

insert  into `orders`(`order_id`,`customer_name`,`status`,`order_date`,`expected_delivery_date`,`created_at`) values 
('NS-1001','Jane Doe','Shipped','2026-08-10','2026-08-15','2026-08-15 12:25:02'),
('NS-1002','John Smith','Processing','2026-08-12','2026-08-18','2026-08-15 12:25:02'),
('NS-1003','Amaka Obi','Delivered','2026-08-01','2026-08-06','2026-08-15 12:25:02'),
('NS-1004','Liam Chen','Out for Delivery','2026-08-11','2026-08-14','2026-08-15 12:25:02'),
('NS-1005','Grace Wanjiru','Shipped','2026-08-09','2026-08-16','2026-08-15 12:25:02'),
('NS-1006','David Kim','Processing','2026-08-13','2026-08-19','2026-08-15 12:25:02'),
('NS-1007','Fatima Ali','Delivered','2026-07-28','2026-08-02','2026-08-15 12:25:02'),
('NS-1008','Peter Otieno','Shipped','2026-08-10','2026-08-17','2026-08-15 12:25:02'),
('NS-1009','Sarah Johnson','Processing','2026-08-13','2026-08-20','2026-08-15 12:25:02'),
('NS-1010','Michael Njoroge','Out for Delivery','2026-08-12','2026-08-14','2026-08-15 12:25:02'),
('NS-1011','Emily Davis','Delivered','2026-08-02','2026-08-07','2026-08-15 12:25:02'),
('NS-1012','Brian Mwangi','Shipped','2026-08-11','2026-08-16','2026-08-15 12:25:02'),
('NS-1013','Aisha Bello','Processing','2026-08-14','2026-08-21','2026-08-15 12:25:02'),
('NS-1014','Tom Walker','Delivered','2026-07-30','2026-08-04','2026-08-15 12:25:02'),
('NS-1015','Grace Adeyemi','Shipped','2026-08-09','2026-08-15','2026-08-15 12:25:02'),
('NS-1016','James Muriuki','Out for Delivery','2026-08-13','2026-08-14','2026-08-15 12:25:02'),
('NS-1017','Linda Park','Processing','2026-08-13','2026-08-19','2026-08-15 12:25:02'),
('NS-1018','Kevin Otieno','Shipped','2026-08-08','2026-08-15','2026-08-15 12:25:02'),
('NS-1019','Nancy Wambui','Delivered','2026-08-03','2026-08-08','2026-08-15 12:25:02'),
('NS-1020','Chris Mwaura','Processing','2026-08-14','2026-08-20','2026-08-15 12:25:02');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
