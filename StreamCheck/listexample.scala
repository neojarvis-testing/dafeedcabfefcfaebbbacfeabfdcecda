object ListExample {
  def main(args: Array[String]): Unit = {
    val immutableList = List(1, 2, 3)
    val updatedList = immutableList :+ 4  // Adds an element, returns new list

    var mutableList = scala.collection.mutable.ListBuffer(1, 2, 3)
    mutableList += 4  // Modifies original list

    println(s"Immutable: $updatedList | Mutable: $mutableList")
  }
}

