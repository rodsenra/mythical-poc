class Review
  def self.find(id)
    JSON.parse(RestClient.get("http://10.2.180.22:5100/data/reviews/#{id}"))
  end
  
  def self.search(q)
    JSON.parse(RestClient.get("http://10.2.180.22:5100/data/reviews?q=#{q}"))
  end
end
