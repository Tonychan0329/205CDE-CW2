-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 19, 2020 at 09:55 PM
-- Server version: 5.7.29-0ubuntu0.18.04.1
-- PHP Version: 7.2.24-0ubuntu0.18.04.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `eshop`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `admin_email` varchar(200) NOT NULL,
  `admin_password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `admin_email`, `admin_password`) VALUES
(1, 'tony@gmail.com', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `cart_id` int(100) NOT NULL,
  `userId` int(11) DEFAULT NULL,
  `productId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `pd_id` int(10) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `image` text NOT NULL,
  `price` double NOT NULL,
  `stock` int(11) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`pd_id`, `name`, `code`, `image`, `price`, `stock`, `description`, `status`) VALUES
(1, 'Mask_KF94', 'KF94', 'product1.jpg', 25, 100, 'The_effect_of_blocking_droplet_infection_is_99.9%!_Bacterial_filtration_efficiency_is_higher_than_94%!', 'ON_SALE'),
(2, '3M_Mask_N95', 'N95', 'product2.jpg', 50, 50, 'BFE_99%,VFE_99%,PFE_99%', 'ON_SALE'),
(3, 'Alcohol_Wet_Wipes', 'KF94', 'product3.jpg', 200, 100, 'wipe_down_whatever_surface_you\'d_like_to_clean_~at_least_60%_alcohol', 'ON_SALE'),
(4, 'Hand_Sanitizr', 'KF94', 'product4.jpg', 25, 60, 'No_washing,quick_drying,easy_to_use,mild_hand_protection', 'ON_SALE'),
(5, 'Rubbing_Alcohol_50ml/2', 'KF94', 'product5.jpg', 40, 100, '70%_First_Aid_Antiseptic_at_Walgreens', 'ON_SALE'),
(6, 'Rubbing_Alcohol_1000ml', 'RA10', 'product6.jpg', 70, 100, '70%_First_Aid_Antiseptic_at_Walgreens', 'ON_SALE'),
(9, 'Mask_30pie', 'JM30', 'product7.jpg', 300, 50, 'BFE_99%_VFE_99%_PFE_99%', 'ON_SALE'),
(10, 'Mask_7pie', 'JM7', 'product8.jpg', 100, 50, 'BFE_99%_VFE_99%_PFE_99%', 'ON_SALE'),
(12, 'mask_50/pie', 'MK55', 'product9.jpg', 300, 100, 'BFE_99%_VFE_99%_PFE_99%', 'SOLD_OUT');

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--

CREATE TABLE `reservation` (
  `reser_id` int(11) NOT NULL,
  `reser_user_id` int(11) DEFAULT NULL,
  `reser_phone` varchar(50) DEFAULT NULL,
  `pd_id` int(11) DEFAULT NULL,
  `pd_name` varchar(100) DEFAULT NULL,
  `reser_amount` int(11) DEFAULT NULL,
  `reser_user_email` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `reservation`
--

INSERT INTO `reservation` (`reser_id`, `reser_user_id`, `reser_phone`, `pd_id`, `pd_name`, `reser_amount`, `reser_user_email`) VALUES
(2, NULL, '94348358', NULL, 'Mask_30pie', 3, 'tonychan871@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(8) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(200) NOT NULL,
  `firstName` text NOT NULL,
  `lastName` text NOT NULL,
  `address` text NOT NULL,
  `city` text NOT NULL,
  `country` text NOT NULL,
  `phone` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `password`, `email`, `firstName`, `lastName`, `address`, `city`, `country`, `phone`) VALUES
(2, '1234', 'tonychan871@gmail.com', 'tony', 'chan', 'Hongkong', 'Kong', 'Hongkong', '67348322');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cart_id`),
  ADD KEY `userId` (`userId`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`pd_id`);

--
-- Indexes for table `reservation`
--
ALTER TABLE `reservation`
  ADD PRIMARY KEY (`reser_id`),
  ADD KEY `reser_user_id` (`reser_user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `cart_id` int(100) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `pd_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
--
-- AUTO_INCREMENT for table `reservation`
--
ALTER TABLE `reservation`
  MODIFY `reser_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `reservation`
--
ALTER TABLE `reservation`
  ADD CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`reser_user_id`) REFERENCES `users` (`user_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
