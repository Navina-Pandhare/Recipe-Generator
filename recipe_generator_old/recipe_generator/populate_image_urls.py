import pandas as pd

FILE = "recipes_MASTER_FINAL.csv"
df = pd.read_csv(FILE)

# Normalize first (CRITICAL)
df["cuisine"] = df["cuisine"].str.strip().str.title()
df["category"] = df["category"].str.strip().str.title()

# -------------------------------------------------
# 1. Ensure image_url column exists
# -------------------------------------------------
if "image_url" not in df.columns:
    df["image_url"] = ""


# -------------------------------------------------
# 2. Override for popular recipes (optional but recommended)
# -------------------------------------------------
RECIPE_IMAGES = {
    "Vegetable Pulao": "https://media.istockphoto.com/id/980078660/photo/indian-vegetable-pulav-or-biryani-made-using-basmati-rice-served-in-a-ceramic-bowl-selective.jpg?s=1024x1024&w=is&k=20&c=ydu4zVDwAaDx_RTb3v70Yif1348nItnSLr41n8zyAxk=",
    "Paneer Butter Masala" : "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Chicken Curry" : "https://images.unsplash.com/photo-1631292784640-2b24be784d5d?q=80&w=580&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Aloo Gobi" : "https://media.istockphoto.com/id/1153272097/photo/aloo-gobi-with-rice-and-chapati-indian-cuisine-vegetarian-dish-decorated-with-lemon-and.jpg?s=1024x1024&w=is&k=20&c=9hnNGL1_GyqCdw-a_GtImncEcRLtT5lyCx-uj15tPgw=",
    "Chicken Alfredo Pasta" : "https://media.istockphoto.com/id/1159438262/photo/one-pot-chicken-alfredo-pasta-directly-above-photo.jpg?s=1024x1024&w=is&k=20&c=wt7eshRZGbouaPCQoO6Q-0E6a_pcTXW5a9XX_MB8klo=",
    "Vegetable Fried Rice" : "https://media.istockphoto.com/id/2007197407/photo/chinese-cuisine-fried-rice-with-vegetables-fried-rice-in-plate-on-table.jpg?s=1024x1024&w=is&k=20&c=0WIrtteX1qHipqL6SPDB7x7vNkq0_zVxDSPLHpMDHQ0=",
    "Chicken Manchurian": "https://media.istockphoto.com/id/667661262/photo/chicken-manchurian-indian-spicy-curry-food.jpg?s=1024x1024&w=is&k=20&c=ceks1yNnkCW4PXUy8mCdEfeGnWyfTm-to059GZL-zFM=",
    "Chicken Chow Mein" : "https://plus.unsplash.com/premium_photo-1661432484710-90bd17326a97?q=80&w=1032&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Chicken Garlic Noodles" : "https://images.unsplash.com/photo-1741243412484-558eb91fe8c7?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Chicken Szechuan Noodles" : "https://images.unsplash.com/photo-1741243412484-558eb91fe8c7?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Chicken Hakka Noodles" : "https://plus.unsplash.com/premium_photo-1661432484710-90bd17326a97?q=80&w=1032&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Vegetable Noodles" : "https://images.unsplash.com/photo-1757445060049-0531425f8643?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", 
    "Grilled Chicken Sandwich" : "https://images.unsplash.com/photo-1730312382518-d8001e2558db?q=80&w=996&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Vegetable Soup" : "https://plus.unsplash.com/premium_photo-1705851313909-97dbf2bf54d6?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Chinese Vegetable Soup" : "https://plus.unsplash.com/premium_photo-1705851313909-97dbf2bf54d6?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Vegetable Manchow Soup" : "https://media.istockphoto.com/id/1331132332/photo/vegetable-manchow-soup.jpg?s=1024x1024&w=is&k=20&c=mZbuAr4_2G7xRGEd6wMv92pmTV3m0OC74bPPTNQqu-g=",
    "Hot and Sour Soup" : "https://media.istockphoto.com/id/1331132332/photo/vegetable-manchow-soup.jpg?s=1024x1024&w=is&k=20&c=mZbuAr4_2G7xRGEd6wMv92pmTV3m0OC74bPPTNQqu-g=",
    "Chicken Soup" : "https://images.unsplash.com/photo-1665594051407-7385d281ad76?q=80&w=386&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Chicken Hot and Sour Soup" : "https://media.istockphoto.com/id/1333237441/photo/hot-and-sour-soup.jpg?s=1024x1024&w=is&k=20&c=FHAebmIZGZ-7JEn14PnZhZiW-OVBywgwVGRAGnqvkiU=",
    "Hummus" : "https://plus.unsplash.com/premium_photo-1663853051786-16613cb8ef0d?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Falafel" : "https://images.unsplash.com/photo-1637861004714-49fa0ccbb993?q=80&w=379&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Falafel Balls" : "https://images.unsplash.com/photo-1637861004714-49fa0ccbb993?q=80&w=379&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Fish Curry" : "https://images.unsplash.com/photo-1654863404432-cac67587e25d?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Chicken Biryani": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Tomato Soup" : "https://images.unsplash.com/photo-1629978444632-9f63ba0eff47?q=80&w=871&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Garlic Bread" : "https://plus.unsplash.com/premium_photo-1711752902734-a36167479983?q=80&w=388&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Chicken Dumplings" : "https://plus.unsplash.com/premium_photo-1661602289442-be921f526ec0?q=80&w=871&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Chicken Momos" : "https://plus.unsplash.com/premium_photo-1661602289442-be921f526ec0?q=80&w=871&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Chicken Tacos" : "https://media.istockphoto.com/id/941591492/photo/homemade-chicken-tacos-with-onion.jpg?s=1024x1024&w=is&k=20&c=RNc8Ns12KPBxAZR3Z5WIUToM-5yLwKxunbBhDPK1FHM=",
    "Chicken Pizza" : "https://media.istockphoto.com/id/185280728/photo/grilled-chicken-and-roasted-pepper-pizza.jpg?s=1024x1024&w=is&k=20&c=bX_sS4-7JfyX5d-IHuyvxBq0iGwGhZQS3QSIbIpr2tk=",
    "Chicken Stew" : "https://media.istockphoto.com/id/1085446276/photo/homemade-french-coq-au-vin-chicken.jpg?s=1024x1024&w=is&k=20&c=m3Gy1NPnngWA_ocDGoBycBs8BQHXl1CVJxgODIXkYR0=",
    "Chicken Risotto" : "https://media.istockphoto.com/id/1142419934/photo/chicken-spinach-and-rice-casserole.jpg?s=1024x1024&w=is&k=20&c=fxrSMq4XSOMks7VLQLsbdPnE7QNhXWTnVwZnOKQVh_0=",
    "Chicken Bruschetta" : "https://media.istockphoto.com/id/954487780/photo/tasty-crunchy-italian-snack-bruschetta-with-grilled-chicken-gar.jpg?s=1024x1024&w=is&k=20&c=urnvdkHIvAsv9FVT7oU6HvO8ztx8ug21GM27qVwvP4g=",
    "Greek Salad" : "https://plus.unsplash.com/premium_photo-1690561082636-06237f98bfab?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Chicken Kebab" : "https://plus.unsplash.com/premium_photo-1663854478523-877ed0dde4af?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Shawarma Wrap" : "https://images.unsplash.com/photo-1762284513096-e411d20c1a4d?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Pancakes" : "https://images.unsplash.com/photo-1612182062633-9ff3b3598e96?q=80&w=419&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Pancake Stack with Syrup" : "https://images.unsplash.com/photo-1612182062633-9ff3b3598e96?q=80&w=419&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Fruit Salad" : "https://images.unsplash.com/photo-1658431618300-a69b07fb5782?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Veg Fried Rice" : "https://media.istockphoto.com/id/1292618457/photo/healthy-and-tasty-veg-fried-rice-made-of-mixed-veggies-served-in-bowl-over-a-rustic-wooden.jpg?s=1024x1024&w=is&k=20&c=ehbTO6Pj5OHb6oqw75rR5MHSNitpiFGZM2v0QF00VeM=",
    "Veg Garlic Rice" : "https://media.istockphoto.com/id/1292618457/photo/healthy-and-tasty-veg-fried-rice-made-of-mixed-veggies-served-in-bowl-over-a-rustic-wooden.jpg?s=1024x1024&w=is&k=20&c=ehbTO6Pj5OHb6oqw75rR5MHSNitpiFGZM2v0QF00VeM=",
    "Mexican Chicken Rice Bowl" : "https://media.istockphoto.com/id/2163190827/photo/rice-bowl-with-pulled-chicken-carnitas-cherry-tomatoes-avocado-peppers-close-up-horizontal.jpg?s=1024x1024&w=is&k=20&c=BRhbjtNLhe0SkiUM4_zmRlTfucWFaifCqBKl0DKxhwo=",
    "Paneer Pulao": "https://media.istockphoto.com/id/1197995878/photo/vegetarian-paneer-biryani-or-panir-pulav-popular-indian-food.jpg?s=1024x1024&w=is&k=20&c=7dK-jnLgVEaGbTBRtwaKiu4lDt9gIfVxbzYhyv-TeFY=",
    "Chicken Fried Rice" : "https://images.unsplash.com/photo-1603133872878-684f208fb84b?q=80&w=725&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Veg Hakka Noodles" : "https://images.unsplash.com/photo-1741243412484-558eb91fe8c7?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Dahi Kachori" : "https://media.istockphoto.com/id/1226693912/photo/indian-traditional-spicy-food-item-dahivada-or-dahi-vada-served-in-a-bowl.jpg?s=1024x1024&w=is&k=20&c=-RQD4MvR6vuJE0-U8AYJcfteNZeoeQBvKNCJSwd9c94=",
    "Classic Rice Kheer" : "https://media.istockphoto.com/id/1177578838/photo/rice-kheer-rice-pudding-chawal-ki-khir.jpg?s=1024x1024&w=is&k=20&c=vc1IIrwWwFfpo31p3Bh45d8K6-B6AEtg-KORNEQM-_M=",
    "Gajar Ka Halwa": "https://media.istockphoto.com/id/1208754471/photo/gajar-ka-halwa.jpg?s=1024x1024&w=is&k=20&c=bS1tDrUJ82TCtAeQPrtTb_JgJqb-cmHSEHR0ZU_mZGg=",
    "Suji Halwa" : "https://media.istockphoto.com/id/1328118094/photo/semolina-banana-pudding-a-fluffy-indian-pudding-made-of-semolina-ghee-sugar-bananas-and.jpg?s=1024x1024&w=is&k=20&c=ifs-3ZpPPxzh_brSMpxUqQLJv9NQ7naJnnu_j1VcW6k=",
    "Besan Ladoo" : "https://media.istockphoto.com/id/1909959228/photo/moong-dal-laddu-a-protein-rich-indian-sweet-ball-made-of-lentils-almonds-and-jaggery-as.jpg?s=1024x1024&w=is&k=20&c=USamDr9Q8RzZtztxYSphfwHAcPF-tTMiC3y4lCTRDX0=",
    "Shrikhand" : "https://media.istockphoto.com/id/978402772/photo/shrikhand-or-srikhand-is-an-indian-dessert-made-of-strained-yogurt-garnished-with-dry-fruits.jpg?s=1024x1024&w=is&k=20&c=_kvO8aJSpsZDSax3flfsOeGXMhV0KPF4nnrtbMXo7e0=",
    "Rasmalai" : "https://media.istockphoto.com/id/515853026/photo/traditional-rasmalai-or-ras-malai-indian-dessert-bengali-sweet.jpg?s=1024x1024&w=is&k=20&c=gSOKfjR5dKCrePmLwfhFLDkCpYIL6QjlzUM7jo113ZA=",
    "New York Cheesecake" : "https://media.istockphoto.com/id/1167344045/photo/cheesecake-slice-new-york-style-classical-cheese-cake.jpg?s=1024x1024&w=is&k=20&c=ii_k4Dd3oAwOeFptRBtZ9QTT1yve8NMUKDD37XZ9dg0=",
    "Belgian Waffles" : "https://media.istockphoto.com/id/478567847/photo/waffles.jpg?s=1024x1024&w=is&k=20&c=ZigbMZELOWWjZ8QFkVcKJy_R6RtHuWGcXVlHBFv_v8Y=",
    "Chocolate Brownies" : "https://media.istockphoto.com/id/168731372/photo/fresh-homemade-chocolate-brownie.jpg?s=1024x1024&w=is&k=20&c=DpEGqN2jWGViFGe85e4scXDRQVIhjrjNqG1RqFdppL4=",
    "Classic Churros" : "https://media.istockphoto.com/id/2154912399/photo/churros-with-hot-chocolate-sauce-sugar-and-cinnamon.jpg?s=1024x1024&w=is&k=20&c=mUYE-YRrtScnnTE7FNiAtzkLS-qkU0YhLavvnSn2wCw=",
    "Fruit Yogurt Parfait" : "https://media.istockphoto.com/id/639376412/photo/blueberry-raspberry-parfaits-in-mason-jars-still-life-against-wood.jpg?s=1024x1024&w=is&k=20&c=c9hfqjjBFhAHi9Tj7YhKusKSIDP0puM-77Ea8GCmV5s=",
    "Chocolate Mousse" : "https://media.istockphoto.com/id/623897390/photo/chocolate-mousse.jpg?s=1024x1024&w=is&k=20&c=7XJOoK0lp6On1j7TabrFms34pQ3OnBZYpGxsq3cBuJw=",
    "Molten Chocolate Cookies" : "https://media.istockphoto.com/id/1499766130/photo/chocolate-fondant-lava-cake.jpg?s=1024x1024&w=is&k=20&c=qwcrHw2tVzeQdx2MOdwYYTNdxzWNopqGQ9qk4p5dFa4=",
    "Strawberry Shortcake" : "https://media.istockphoto.com/id/171107631/photo/strawberry-shortcake.jpg?s=1024x1024&w=is&k=20&c=vuep11sDJCLpuYs4u7cKVszt0jXeIopScJ59k50tNsI=",
    "Chocolate Banana Bread" : "https://media.istockphoto.com/id/1147312072/photo/banana-bread-loaf-on-wooden-table.jpg?s=1024x1024&w=is&k=20&c=ryiVDqcftZkRstmVZphB6k5Q6USGDgWGdg_zVB8ii4M=",
    "Chocolate Lava Cake" : "https://media.istockphoto.com/id/1255982848/photo/homemade-chocoalte-molten-lava-cake.jpg?s=1024x1024&w=is&k=20&c=5KFwtJ4Lw1M2PjJZa5y-AbSGP_SX2SExE2LL3lU_cGM=",
    "Margherita Pizza": "https://media.istockphoto.com/id/1414575281/photo/a-delicious-and-tasty-italian-pizza-margherita-with-tomatoes-and-buffalo-mozzarella.jpg?s=1024x1024&w=is&k=20&c=bwoUzONnFgIK65TQ7uUeSAlM78h-gCmKSR3nnGhb6AI=",
    "Shakshuka": "https://images.unsplash.com/photo-1590412200988-a436970781fa?q=80&w=435&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Bean Burrito": "https://plus.unsplash.com/premium_photo-1664478244517-513dc18af854?q=80&w=657&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Lentil Soup": "https://plus.unsplash.com/premium_photo-1712678665724-7c3faa117a2d?q=80&w=871&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Chicken Stir Fry": "https://media.istockphoto.com/id/1312622136/photo/stir-fried-cashew-chicken-in-a-bowl-garnished-with-fresh-thai-basil-and-lemon.jpg?s=1024x1024&w=is&k=20&c=Y2KCGrslJb_LlSTciiRBZh_Apl3yf2zAhZVUrQmuljw=",
    "Chicken Risotto": "https://images.unsplash.com/photo-1653981608672-aea09b857b20?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "Kung Pao Chicken": "https://media.istockphoto.com/id/1225394561/photo/image-of-spicy-kung-pao-chicken-takeaway-meal-in-black-plastic-disposable-container-with.jpg?s=1024x1024&w=is&k=20&c=ziaaZ35Nxj3IqsSVeBrdzPnKGLyq5tGns1v6hgApv1k=",
    "Sweet and Sour Chicken": "https://media.istockphoto.com/id/1459160790/photo/sesame-shrimp-roll-spicy-stir-fry-and-sweet-and-sour-sauce-served-dish-isolated-on-wooden.jpg?s=1024x1024&w=is&k=20&c=1pFBr8rECko9Tyee5qLMwbDynbCbz2Nm3z054zdWH6k=",
    "Mushroom Risotto": "https://media.istockphoto.com/id/1369183332/photo/risotto-with-brown-champignon-mushrooms.jpg?s=1024x1024&w=is&k=20&c=xRyu6oR1qIqaQbfJgDKuHa4q_Z4WeADLGmS7PC3UF_Q=",
    "Chicken Lasagna": "https://media.istockphoto.com/id/1588616839/photo/brazilian-food.jpg?s=1024x1024&w=is&k=20&c=N9VGt693yFu6TsrZ6vKafaCt9w4dmFvSB1YuxKwq_LY=",
    "Italian Tomato Bruschetta": "https://media.istockphoto.com/id/481765835/photo/homemade-italian-bruschetta-appetizer.jpg?s=1024x1024&w=is&k=20&c=SfHpZR2YSRtyx-tYEG-SrAZWG-lNWq-IWREzPy1mx7w=",
    "Middle Eastern Spiced Chicken Pilaf": "https://media.istockphoto.com/id/1368187260/photo/groats-freekeh-with-chicken-is-such-a-well-rounded-arabic-meal-closeup-in-the-plate-horizontal.jpg?s=1024x1024&w=is&k=20&c=l_KjrdbjOVpyN0sDizOa6dTR0EpSUApQkX-IX5hKOWs=",
    "Chicken Teriyaki Rice Bowl": "https://media.istockphoto.com/id/698942358/photo/grilled-chicken-breast-with-teriyaki-sauce-over-steamed-rice.jpg?s=1024x1024&w=is&k=20&c=5xlLv1CY53DPkfo90XcRUDvLXruAy0-JoPafg8I7i6E=",
    "Vegetable Samosa": "https://media.istockphoto.com/id/848708640/photo/asian-food-vegetarian-samsa-with-tomato-sauce-and-herbs-dark-background.jpg?s=1024x1024&w=is&k=20&c=PgIF0-Xdodnhm2qWQdOMg-JulQ3ScJwqfNNP4lisTTE=",
    "Chicken Seekh Kebab": "https://media.istockphoto.com/id/501027041/photo/behrai-kabab-1.jpg?s=1024x1024&w=is&k=20&c=WBomfoKQLVwCSJcSARjcXjNMOSlBBHjUAnKFevrImwk=",
    "Chicken Puff Pastry": "https://media.istockphoto.com/id/627675946/photo/homemade-pie-stuffed-with-broccoli-chicken-and-cheese.jpg?s=1024x1024&w=is&k=20&c=a8E2LppyLYyBIKdRD1Sp8oQwNaNrhr_gqJ_M0ksB5RM=",
    "Chicken Piccata": "https://media.istockphoto.com/id/1126510757/photo/pan-seared-lemon-chicken-picatta-in-a-creamy-sauce-perfect-ketogenic-diet-food.jpg?s=1024x1024&w=is&k=20&c=xYWb0wjysd7XJssBs2PrRKjlKsfAIenl2L9pbS7Fm14=",
    "Chicken Stuffed Puff Pastry": "https://media.istockphoto.com/id/627675946/photo/homemade-pie-stuffed-with-broccoli-chicken-and-cheese.jpg?s=1024x1024&w=is&k=20&c=a8E2LppyLYyBIKdRD1Sp8oQwNaNrhr_gqJ_M0ksB5RM=",
    "Chicken Popcorn Bites": "https://media.istockphoto.com/id/1162655243/photo/crispy-popcorn-chicken-on-wooden-board-and-dipping-sauce.jpg?s=1024x1024&w=is&k=20&c=zvNK7Sgl5HRPhzq2mBGqvno1w8oKApODjM0zVYoONzM=",
}

for recipe, img_url in RECIPE_IMAGES.items():
    df.loc[df["recipe_name"] == recipe, "image_url"] = img_url

# -------------------------------------------------
# 2. CUISINE + CATEGORY IMAGE MAP (MEDIUM PRIORITY)
# -------------------------------------------------
IMAGE_MAP = {
    ("Indian", "Breakfast"): "Images/Indian Breakfast.jpg",
    ("Indian", "Lunch"): "Images/Indian Lunch.jpg",
    ("Indian", "Snack"): "Images/Indian Snacks.jpg",
    ("Indian", "Dessert"): "Images/Indian Desserts.jpg",
    ("Indian", "Dinner"): "Images/Indian Dinner.jpg",

    ("Chinese","Breakfast"): "Images/Chinese Breakfast.jpg",
    ("Chinese", "Snack"): "Images/Chinese Snacks.jpg",
    ("Chinese", "Lunch"): "Images/Chinese Food.jpg",
    ("Chinese", "Dinner"): "Images/Chinese Food.jpg",

    ("Italian", "Breakfast"): "Images/Italian Breakfast.jpg",
    ("Italian", "Lunch"): "Images/Italian Food.jpg",
    ("Italian", "Dinner"): "Images/Italian Food.jpg",
    ("Italian", "Snack"): "Images/Italian Snacks.jpg",
    ("Italian", "Dessert"): "Images/Italian Desserts.jpg",

    ("Mexican", "BreakFast") : "Images/Mexican Food.jpg",
    ("Mexican", "Lunch") : "Images/Mexican Food.jpg",
    ("Mexican", "Dinner") : "Images/Mexican Food.jpg",
    ("Mexican", "Snack") : "Images/Mexican Food.jpg",

    ("Middle Eastern", "Breakfast") : "Images/Mid East Breakfast.jpg",
    ("Middle Eastern", "Lunch") : "Images/Middle Eastern Food.jpg",
    ("Middle Eastern", "Dinner") : "Images/Middle Eastern Food.jpg",
    ("Middle Eastern", "Snack") : "Images/Mid East Snacks.jpg",

    ("Continental", "breakfast"): "Images/Cont Breakfast.jpg",
    ("Continental", "Dessert"): "Images/Cont Desserts.jpg",
    ("Continental", "Lunch"): 'Images/Cont Lunch.jpg',
    ("Continental", "Dinner"): 'Images/Cont Dinner.jpg',
    ("Continental", "Snack"): 'Images/Cont Snacks.jpg',
}

for (cuisine, category), img_url in IMAGE_MAP.items():
    df.loc[
        (df["cuisine"] == cuisine) &
        (df["category"] == category) &
        (df["image_url"].isna() | (df["image_url"] == "")),
        "image_url"
    ] = img_url

# -------------------------------------------------
# 2. Cuisine-based fallback images
# -------------------------------------------------
CUISINE_IMAGES = {
    "Indian": "Images/Indian Lunch.jpg",
    "Italian": "Images/Italian Lunch.jpg",
    "Chinese": "Images/Chinese Food.jpg",
    "Mexican": "Images/Mexican Food.jpg",
    "Middle Eastern": "/Images/Middle Eastern Food.jpg",
    "Continental": "Images/Cont Lunch.jpg"
}

# Fill image_url only if empty
for cuisine, img_url in CUISINE_IMAGES.items():
    df.loc[
        (df["cuisine"] == cuisine) &
        (df["image_url"].isna() | (df["image_url"] == "")),
        "image_url"
    ] = img_url

# -------------------------------------------------
# 5. FINAL SAFETY FALLBACK (NO BLANKS ALLOWED)
# -------------------------------------------------
df["image_url"].replace(
    "",
    "https://via.placeholder.com/400x250?text=Recipe+Image",
    inplace=True
)

# -------------------------------------------------
# 4. Save updated dataset
# -------------------------------------------------
df.to_csv(FILE, index=False)
print("Image URLs populated successfully.")
