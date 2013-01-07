Techtudo::Application.routes.draw do
  resources :reviews, only: :show
end
