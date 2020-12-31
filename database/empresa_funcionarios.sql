-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 13-Nov-2020 às 20:58
-- Versão do servidor: 10.1.38-MariaDB
-- versão do PHP: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `empresa_funcionarios`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `funcionarios`
--

CREATE TABLE `funcionarios` (
  `id` int(11) NOT NULL,
  `nome` varchar(30) NOT NULL,
  `cpf` varchar(11) NOT NULL,
  `senha` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `funcionarios`
--

INSERT INTO `funcionarios` (`id`, `nome`, `cpf`, `senha`) VALUES
(1, 'JUNIOR MOREIRA DA SILVA', '01020304050', '1234');

-- --------------------------------------------------------

--
-- Estrutura da tabela `monitoria_funcionarios`
--

CREATE TABLE `monitoria_funcionarios` (
  `Id` int(11) NOT NULL,
  `Operador` varchar(30) NOT NULL,
  `HoraLogin` varchar(8) NOT NULL,
  `HoraInical` varchar(8) NOT NULL,
  `HoraFinal` varchar(8) NOT NULL,
  `TempGasto` varchar(8) NOT NULL,
  `TempProgramado` varchar(8) NOT NULL,
  `CodigoPeca` varchar(8) NOT NULL,
  `OS` varchar(8) NOT NULL,
  `TempGastoExt` varchar(8) NOT NULL,
  `VezTempExt` varchar(8) NOT NULL,
  `tempOperando` varchar(8) DEFAULT NULL,
  `tipo` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `monitoria_funcionarios`
--

INSERT INTO `monitoria_funcionarios` (`Id`, `Operador`, `HoraLogin`, `HoraInical`, `HoraFinal`, `TempGasto`, `TempProgramado`, `CodigoPeca`, `OS`, `TempGastoExt`, `VezTempExt`, `tempOperando`, `tipo`) VALUES
(49, 'JUNIOR MOREIRA DA SILVA', '10:51:25', '10:51:41', '10:52:12', '00:00:30', '00:01:00', '1010', '01', '00:00:00', '0', '00:00:00', 'Nova OS'),
(50, 'JUNIOR MOREIRA DA SILVA', '10:12:36', '10:25:57', '10:26:21', '00:01:00', '00:01:00', '1010', '01', '00:10:23', '2', '00:00:00', 'Retrabalhar OS');

-- --------------------------------------------------------

--
-- Estrutura da tabela `pausa_funcionarios`
--

CREATE TABLE `pausa_funcionarios` (
  `id` int(11) NOT NULL,
  `operador` varchar(50) DEFAULT NULL,
  `codigoPeca` varchar(8) DEFAULT NULL,
  `OS` varchar(8) DEFAULT NULL,
  `motivoPause` varchar(20) DEFAULT NULL,
  `horaPause` varchar(8) DEFAULT NULL,
  `horaRetomada` varchar(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estrutura da tabela `pecas_codigo`
--

CREATE TABLE `pecas_codigo` (
  `id` int(11) NOT NULL,
  `peca` varchar(10) NOT NULL,
  `codigo` varchar(4) NOT NULL,
  `hora` varchar(2) NOT NULL,
  `minuto` varchar(2) NOT NULL,
  `segundo` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `pecas_codigo`
--

INSERT INTO `pecas_codigo` (`id`, `peca`, `codigo`, `hora`, `minuto`, `segundo`) VALUES
(1, 'prensa', '2525', '01', '00', '00'),
(2, 'pino', '1010', '00', '01', '00'),
(3, 'chav', '2020', '00', '02', '00'),
(4, 'broca', '1212', '00', '06', '00'),
(5, 'porca', '5050', '00', '05', '00');

-- --------------------------------------------------------

--
-- Estrutura da tabela `supervisor_admin`
--

CREATE TABLE `supervisor_admin` (
  `senha` varchar(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `supervisor_admin`
--

INSERT INTO `supervisor_admin` (`senha`) VALUES
('0405123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `funcionarios`
--
ALTER TABLE `funcionarios`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `monitoria_funcionarios`
--
ALTER TABLE `monitoria_funcionarios`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `pausa_funcionarios`
--
ALTER TABLE `pausa_funcionarios`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pecas_codigo`
--
ALTER TABLE `pecas_codigo`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `funcionarios`
--
ALTER TABLE `funcionarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `monitoria_funcionarios`
--
ALTER TABLE `monitoria_funcionarios`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `pausa_funcionarios`
--
ALTER TABLE `pausa_funcionarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pecas_codigo`
--
ALTER TABLE `pecas_codigo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
