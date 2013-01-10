class Review
  def self.find(id)
    JSON.parse(RestClient.get("http://localhost:5100/data/reviews/#{id}"))
  end
  
  def self.search(q)
    JSON.parse(RestClient.get("http://localhost:5100/data/reviews?q=#{q}"))
  end
end
