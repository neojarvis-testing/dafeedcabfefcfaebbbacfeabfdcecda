object BookExample {
  class Book(val title: String, val price: Double)

  object Book {
    def apply(title: String, price: Double): Book = new Book(title, price)
  }

  def main(args: Array[String]): Unit = {
    val b1 = Book("Scala Basics", 399.99)
    println(s"${b1.title} - ₹${b1.price}")
  }
}
