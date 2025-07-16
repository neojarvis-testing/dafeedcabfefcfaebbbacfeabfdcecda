object ValVarExample {
  def main(args: Array[String]): Unit = {
    val course = "Scala Programming"
    var progress = 0
    progress += 10
    println(s"Course: $course, Progress: $progress%")
  }
}
