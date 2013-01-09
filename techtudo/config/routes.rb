Techtudo::Application.routes.draw do
  get :busca, to: "buscas#show"
  resources :reviews, only: :show
  root to: "buscas#show"
end
