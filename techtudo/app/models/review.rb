class Review
  def self.find(slug)
    JSON.parse(RestClient.get("http://localhost:5100/data/tech/reviews/#{slug}"))
  end
  
  def self.search(q)
    JSON.parse(RestClient.get("http://localhost:5100/data/reviews?q=#{q}"))
  end
end
