class ReviewsController < ApplicationController
  def show
    @review = RestClient.get("http://localhost:5100/data/reviews/#{params[:id]}")
  end
end
