# NKUST Project Back-End

<details>
<summary>English</summary>

  
# NKUST Project Back-End

This repository contains multiple sub-projects, primarily:

- **`TripWeb_Backend`**: Django-based back-end services (front-end integration planned for 5/20)
- **`TripWeb_NFT_Management`**: Python scripts for minting, transferring, and burning NFTs

Below is a layered directory overview and functional breakdown for each module.

---

## 📁 TripWeb_Backend

A Django project responsible for user authentication, trip orders, and token management. Front-end templates live alongside their corresponding apps under `templates/`.

TripWeb_Backend/
├── manage.py
├── db.sqlite3
├── venv/ # Local virtual environment (gitignored)
├── core/ # Django “project” settings
│ ├── pycache/
│ └── core/
│ ├── init.py
│ ├── settings.py # Global settings (DATABASES, INSTALLED_APPS, etc.)
│ ├── urls.py # Root URL router
│ ├── asgi.py # ASGI entrypoint for async deployments
│ └── wsgi.py # WSGI entrypoint for traditional deployments
├── management/ # Django “apps” for business logic
│ ├── member/ # User management: registration, login, permissions
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ └── urls.py
│ ├── order/ # Trip order management: create, query, cancel
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ └── urls.py
│ ├── tokens/ # NFT token management: mint, list, revoke
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ └── urls.py
│ └── trip/ # Trip data CRUD and category filtering
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ └── urls.py
├── templates/
│ └── registration/ # Django’s built-in auth templates
│ ├── login.html
│ ├── logged_out.html
│ ├── password_reset_form.html
│ ├── password_reset_done.html
│ ├── password_reset_confirm.html
│ └── password_reset_complete.html
└── requirements.txt # Python dependencies (to be added)


---

## 📁 TripWeb_NFT_Management

A set of standalone Python scripts that interact with XRPL (or other blockchains) to manage NFT lifecycles. Each script lives under the project root:

TripWeb_NFT_Management/
├── createAccount.py # Initialize on-chain account & keypair
├── createAccountImplement.py # Advanced account creation routines
├── createTrustLine_SendCurrency.py # Establish trust line & fund account
├── mintAndBurnNFT.py # Mint or burn a single NFT
├── batchMintNFT.py # Batch-mint NFTs from a list
└── buyAndSellNFT.py # Execute NFT buy/sell transactions

</details>

<details>
<summary>中文</summary>

# Nkust Project Back-End

本倉庫包含多個子專案，其中主要分為：

- `TripWeb_Backend`：Django 後端服務（本週預計將前端結合）
- `TripWeb_NFT_Management`：Python 腳本工具，用於 NFT 發行與管理

以下針對這兩個子資料夾做分層結構與功能說明。

---

## 📁 TripWeb_Backend

`TripWeb_Backend` 採用 Django 開發，預計於（5/20）將前端與後端整合於此。前端資料保持在各子層級的 templates 資料夾中。

TripWeb_Backend/
├── manage.py 
├── db.sqlite3 
├── venv/ # 本地虛擬環境（經 .gitignore 處理）
├── core/ # Django project 設定（主專案）
│ ├── pycache/
│ └── core/
│ ├── init.py
│ ├── settings.py # 全域設定（DATABASES、INSTALLED_APPS 等）
│ ├── urls.py 
│ ├── asgi.py 
│ └── wsgi.py 
├── management/ # 有關任何管理相關應用 Django apps
│ ├── member/ # 會員管理：註冊、登入、權限
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ └── urls.py
│ ├── order/ # 行程訂單管理：下單、查詢、取消
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ └── urls.py
│ ├── tokens/ # NFT Token 管理：發行、新增、註銷等
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ └── urls.py
│ └── trip/ # 行程相關及分類查詢
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ └── urls.py
├── templates/registration/ # Django 內建認證流程模板
│ ├── login.html
│ ├── logged_out.html
│ ├── password_reset_form.html
│ ├── password_reset_done.html
│ ├── password_reset_confirm.html
│ └── password_reset_complete.html
└── requirements.txt # 未來將會新增這必要檔案

## 📁 TripWeb_NFT_Management

這一組 Python 腳本負責與 XRPL 或其他鏈上服務串接，執行 NFT 的鑄造、轉帳及燒毀等動作。放在根目錄的 `TripWeb_NFT_Management/`：
TripWeb_NFT_Management/
├── createAccount.py # 建立鏈上帳戶
├── createAccountImplement.py # 帳戶建立進階實作
├── createTrustLine_SendCurrency.py # 設定信任線並發送貨幣
├── mintAndBurnNFT.py # NFT 鑄造與燒毀
├── batchMintNFT.py # 批次鑄造 NFT
└── buyAndSellNFT.py # NFT 買賣交易

</details>







