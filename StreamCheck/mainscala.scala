object FunctionExample {
  def calculate(x: Int, y: Int, ans: (Int, Int) => Int): Int = ans(x, y)

  def main(args: Array[String]): Unit = {
    val sum = calculate(4, 5, (a, b) => a + b)
    println(s"Sum = $sum")  // Output: Sum = 9
  }
}


