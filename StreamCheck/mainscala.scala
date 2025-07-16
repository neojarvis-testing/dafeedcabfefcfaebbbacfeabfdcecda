object DiscountFunction {
  def discount(rate: Double): Double => Double = {
    amount => amount - (amount * rate)
  }

  def main(args: Array[String]): Unit = {
    val tenPercentOff = discount(0.10)
    val finalPrice = tenPercentOff(200)
    println(s"Final Price after 10% discount = $$${finalPrice}")
  }
}

