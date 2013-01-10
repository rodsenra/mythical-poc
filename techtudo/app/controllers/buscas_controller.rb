class BuscasController < ApplicationController
  def show
    @reviews = Review.search(params[:q] || "*")
  end
end
