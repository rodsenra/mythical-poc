class Review
  def self.find(id)
    RestClient.get("http://localhost:5100/data/reviews/#{id}")
  end
end
