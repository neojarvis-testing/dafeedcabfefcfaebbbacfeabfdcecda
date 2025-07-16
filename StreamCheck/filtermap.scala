object FilterMapExample {
  def main(args: Array[String]): Unit = {
    val numbers = List(10, 15, 25, 30)

    val evensDoubled = numbers
      .filter(num => num % 2 == 0)   // keep even numbers
      .map(num => num * 2)          // double each even number

    println(evensDoubled)  // Output: List(20, 60)
  }
}
