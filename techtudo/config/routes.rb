Techtudo::Application.routes.draw do
  get :busca, to: "buscas#show"
  resources :reviews, only: :show
end
