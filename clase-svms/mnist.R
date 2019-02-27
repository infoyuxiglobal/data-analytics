#' Visualize MNIST digit.
#'
#' Display an MNIST digit as an image the hand-written digit represented by the
#' nth row in a data frame.
#'
#' @note Originally based on a function by Brendan O'Connor.
#' @param df Data frame containing MNIST digits.
#' @param n Row index of the digit to display.
#' @param col List of colors to use in the display.
#' @param ... Other arguments passed onto the \code{\link[graphics]{image}}
#' function.
#' @examples
#' \dontrun{
#' # show the fifth digit
#' mnist <- download_mnist()
#' show_digit(mnist, 5)
#' }
#' @export
show_digit <- function(df, n, col = grDevices::gray(12:1 / 12), ...) {
  graphics::image(matrix(as.numeric(df[n, 1:784]), nrow = 28)[, 28:1],
                  col = col, ...)
}

# Base URL of the the MNIST digits dataset website
mnist_url <- "http://yann.lecun.com/exdb/mnist/"

#' Download MNIST
#'
#' Download MNIST database of handwritten digits.
#'
#' Downloads the image and label files for the training and test datasets from
#' \url{http://yann.lecun.com/exdb/mnist} and converts them to a data frame.
#'
#' @format A data frame with 785 variables:
#'
#' \describe{
#' \item{\code{px1}, \code{px2}, \code{px3} ... \code{px784}}{Integer pixel
#'   value, from 0 (white) to 255 (black).}
#' \item{\code{Label}}{The digit represented by the image, in the range 0-9.}
#' }
#'
#' Pixels are organized row-wise. The \code{Label} variable is stored as a
#' factor.
#'
#' There are 70,000 digits in the data set. The first 60,000 are the training
#' set, as found in the \code{train-images-idx3-ubyte.gz} file. The remaining
#' 10,000 are the test set, from the \code{t10k-images-idx3-ubyte.gz} file.
#'
#' For more information see \url{http://yann.lecun.com/exdb/mnist}.
#'
#' @param base_url Base URL that the MNIST files are located at.
#' @param verbose If \code{TRUE}, then download progress will be logged as a
#'   message.
#' @return Data frame containing the MNIST digits.
#' @note Originally based on a function by Brendan O'Connor.
#' @export
#' @examples
#' \dontrun{
#' # download the MNIST data set
#' mnist <- download_mnist()
#'
#' # first 60,000 instances are the training set
#' mnist_train <- head(mnist, 60000)
#' # the remaining 10,000 are the test set
#' mnist_test <- tail(mnist, 10000)
#'
#' # PCA on 1000 random training examples
#' mnist_r1000 <- mnist_train[sample(nrow(mnist_train), 1000), ]
#' pca <- princomp(mnist_r1000[, 1:784], scores = TRUE)
#' # plot the scores of the first two components
#' plot(pca$scores[, 1:2], type = 'n')
#' text(pca$scores[, 1:2], labels = mnist_r1000$Label,
#'      col = rainbow(length(levels(mnist_r1000$Label)))[mnist_r1000$Label])
#'}
#' @export
download_mnist <- function(base_url = mnist_url, verbose = FALSE, local = FALSE) {
  train <- parse_files("train-images-idx3-ubyte.gz",
                       "train-labels-idx1-ubyte.gz",
                       base_url = base_url, verbose = verbose, local = local)
  test <- parse_files("t10k-images-idx3-ubyte.gz",
                      "t10k-labels-idx1-ubyte.gz",
                      base_url = base_url, verbose = verbose, local = local)
  rbind(train, test)
}

# Open Gzipped Binary File at URL
#
# Opens a file at a specified URL and returns the connection for further
# processing. Callers must close the connection when they're done.
#
# @param filename Name of the file to open.
# @param base_url URL of the resource containing the file.
# @param verbose If \code{TRUE}, generate a diagnostic message when the file
# is opened.
# @return Opened connection to the file.
open_binary_file <- function(filename, base_url = mnist_url, verbose = FALSE, local = FALSE) {
  path <- paste0(base_url, filename)
  
  if (local) {
    if (verbose) {
      message("Opening local file ", path)
    }
    gzcon( file(path, "rb") )
  } else {
    if (verbose) {
      message("Downloading ", path)
    }
    gzcon(url(path, "rb"))
  }
  
}

# Parse Image File
#
# Downloads a gzipped MNIST image file.
#
# @param filename The image filename.
# @param base_url URL of the resource containing the \code{filename}.
# @param verbose If \code{TRUE}, generate a diagnostic message as files are
# downloaded.
# @return Vector of integers representing the digits.
parse_image_file <- function(filename, base_url = mnist_url, local = FALSE,
                             verbose = verbose) {
  f <- open_binary_file(filename, base_url = base_url, local = local, verbose = verbose)
  magic <- readBin(f, "integer", n = 1, size = 4, endian = "big")
  if (magic != 2051) {
    stop("First four bytes of image file should be magic number 2051 but was ",
         magic)
  }
  n <- readBin(f, "integer", n = 1, size = 4, endian = "big")
  nrow <- readBin(f, "integer", n = 1, size = 4, endian = "big")
  ncol <- readBin(f, "integer", n = 1, size = 4, endian = "big")
  x <- readBin(f, "integer", n = n * nrow * ncol, size = 1, signed = FALSE)
  close(f)
  matrix(x, ncol = nrow * ncol, byrow = TRUE)
}

# Parse Label File
#
# Downloads a gzipped MNIST label file.
#
# @param filename The label filename.
# @param base_url URL of the resource containing \code{filename}.
# @param verbose If \code{TRUE}, generate a diagnostic message as files are
# downloaded.
# @return Vector of integers representing the digits.
parse_label_file <- function(filename, base_url = mnist_url, verbose = FALSE, local = local) {
  f <- open_binary_file(filename, base_url = base_url, verbose = verbose, local = local)
  magic <- readBin(f, "integer", n = 1, size = 4, endian = "big")
  if (magic != 2049) {
    stop("First four bytes of label file should be magic number 2049 but was ",
         magic)
  }
  n <- readBin(f, "integer", n = 1, size = 4, endian = "big")
  y <- readBin(f, "integer", n = n, size = 1, signed = FALSE)
  close(f)
  y
}

# Parse Image and Label File Pair
#
# Downloads an image file and a corresponding label file, combining
# them into a data frame.
#
# @param image_filename The image filename.
# @param label_filename The label filename corresponding to the images in
#   \code{image_filename}.
# @param base_url URL of the resource containing the files.
# @param verbose If \code{TRUE}, generate a diagnostic message as files are
#   downloaded.
# @return Data frame containing images and labels.
parse_files <- function(image_filename, label_filename, base_url = mnist_url,
                        verbose = FALSE, local = FALSE) {
  df <- as.data.frame(parse_image_file(image_filename, base_url = base_url,
                                       verbose = verbose, local = local))
  names(df) <- paste0("px", 1:ncol(df))
  df$Label <- factor(parse_label_file(label_filename, base_url = base_url,
                                      verbose = verbose, local = local))
  df
}

