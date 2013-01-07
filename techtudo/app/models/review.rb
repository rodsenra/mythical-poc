class Review
  def self.find(id)
    RestClient.get("http://10.2.180.22:5100/data/reviews/#{id}")
  end
end
