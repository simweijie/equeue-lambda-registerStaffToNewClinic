terraform {
  backend "s3" {
    bucket = "nus-iss-equeue-terraform"
    key    = "lambda/registerStaffToNewClinic/tfstate"
    region = "us-east-1"
  }
}
