
import Pkg
Pkg.add("YahooFinance")
Pkg.add(Pkg.PackageSpec(name="DataFrames", version="0.20.2"))
Pkg.add("YahooFinance")
import Pkg
Pkg.activate("bsts_env")  # Creates a new environment in the bsts_env directory
Pkg.add(["CSV", "DataFrames", "Dates", "Turing", "StatsPlots", "Distributions", "YahooFinance", "Statistics", "Random"])
include("bsts_forecast.jl")
