-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 02 Mar 2020, 17:47
-- Wersja serwera: 10.4.11-MariaDB
-- Wersja PHP: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `library`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `books`
--

CREATE TABLE `books` (
  `ID` int(11) NOT NULL,
  `Title` varchar(1000) NOT NULL,
  `Author` varchar(1000) NOT NULL,
  `Signature` varchar(255) NOT NULL,
  `Amount` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `clients`
--

CREATE TABLE `clients` (
  `ID` int(11) NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Lastname` varchar(50) DEFAULT NULL,
  `MonthDATE` int(11) DEFAULT NULL,
  `DayDATE` int(11) DEFAULT NULL,
  `HourDATE` int(11) DEFAULT NULL,
  `MinuteDATE` int(11) DEFAULT NULL,
  `ArrivalTime` float DEFAULT NULL,
  `OrderTime` float DEFAULT NULL,
  `ServiceTime` float DEFAULT NULL,
  `QueueTime` float DEFAULT NULL,
  `Pleased` varchar(3) DEFAULT NULL,
  `BorrowedBook` int(11) DEFAULT NULL,
  `ReturnTime` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`ID`);

--
-- Indeksy dla tabeli `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT dla tabeli `books`
--
ALTER TABLE `books`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `clients`
--
ALTER TABLE `clients`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
