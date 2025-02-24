# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EbayRegisterFromYahooAuction(models.Model):
    id = models.BigAutoField(primary_key=True)
    sku = models.CharField(unique=True, max_length=255)
    ebay_price = models.DecimalField(max_digits=10, decimal_places=2)
    ebay_shipping_price = models.DecimalField(max_digits=10, decimal_places=2)
    final_profit = models.DecimalField(max_digits=10, decimal_places=2)
    yahoo_auction_id = models.CharField(max_length=255)
    yahoo_auction_item_name = models.CharField(max_length=255)
    yahoo_auction_item_price = models.DecimalField(max_digits=10, decimal_places=2)
    yahoo_auction_shipping = models.DecimalField(max_digits=10, decimal_places=2)
    yahoo_auction_end_time = models.DateTimeField()
    update_datetime = models.DateTimeField()
    insert_datetime = models.DateTimeField()
    status = models.ForeignKey('MStatus', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    yahoo_auction_url = models.CharField(max_length=255, blank=True, null=True)
    offer_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ebay_register_from_yahoo_auction'


class EbayTokens(models.Model):
    id = models.BigAutoField(primary_key=True)
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()
    scope = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebay_tokens'


class MCondition(models.Model):
    id = models.BigAutoField(primary_key=True)
    condition_id = models.IntegerField()
    condition_enum = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'm_condition'


class MCountries(models.Model):
    id = models.BigAutoField(primary_key=True)
    country_code = models.CharField(unique=True, max_length=2)
    country_name = models.CharField(max_length=100)
    country_name_jp = models.CharField(max_length=100)
    zone = models.CharField(max_length=1)
    service = models.ForeignKey('MService', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'm_countries'


class MEbayStoreType(models.Model):
    id = models.BigAutoField(primary_key=True)
    store_type = models.CharField(unique=True, max_length=50)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monthly_fee_annual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    free_listings = models.IntegerField()
    listing_fee_over_limit = models.DecimalField(max_digits=4, decimal_places=2)
    final_value_fee = models.DecimalField(max_digits=4, decimal_places=1)
    final_value_fee_category_discount = models.IntegerField()
    international_fee = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'm_ebay_store_type'


class MService(models.Model):
    id = models.BigAutoField(primary_key=True)
    service_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'm_service'


class MSetting(models.Model):
    id = models.BigAutoField(primary_key=True)
    yahoo_client_id = models.CharField(max_length=255, blank=True, null=True)
    yahoo_client_secret = models.CharField(max_length=255, blank=True, null=True)
    ebay_client_id = models.CharField(max_length=255, blank=True, null=True)
    ebay_client_secret = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    ebay_dev_id = models.CharField(max_length=255, blank=True, null=True)
    rate = models.IntegerField(blank=True, null=True)
    deepl_api_key = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    ebay_store_type = models.ForeignKey(MEbayStoreType, models.DO_NOTHING)
    description_template_1 = models.TextField(blank=True, null=True)
    description_template_2 = models.TextField(blank=True, null=True)
    description_template_3 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'm_setting'


class MShipping(models.Model):
    id = models.BigAutoField(primary_key=True)
    zone = models.CharField(max_length=1)
    weight = models.IntegerField()
    basic_price = models.DecimalField(max_digits=10, decimal_places=2)
    service = models.ForeignKey(MService, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'm_shipping'


class MShippingSurcharge(models.Model):
    id = models.BigAutoField(primary_key=True)
    surcharge_type = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    fixed_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    service = models.ForeignKey(MService, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'm_shipping_surcharge'


class MStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    status_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'm_status'


class MTax(models.Model):
    id = models.BigAutoField(primary_key=True)
    rate = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'm_tax'


class MYahooAuctionStatus(models.Model):
    status_name = models.CharField(primary_key=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'm_yahoo_auction_status'


class Oauth2ProviderAccesstoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.TextField()
    expires = models.DateTimeField()
    scope = models.TextField()
    application = models.ForeignKey('Oauth2ProviderApplication', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    source_refresh_token = models.OneToOneField('Oauth2ProviderRefreshtoken', models.DO_NOTHING, blank=True, null=True)
    id_token = models.OneToOneField('Oauth2ProviderIdtoken', models.DO_NOTHING, blank=True, null=True)
    token_checksum = models.CharField(unique=True, max_length=64)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_accesstoken'


class Oauth2ProviderApplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    client_id = models.CharField(unique=True, max_length=100)
    redirect_uris = models.TextField()
    client_type = models.CharField(max_length=32)
    authorization_grant_type = models.CharField(max_length=32)
    client_secret = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    skip_authorization = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    algorithm = models.CharField(max_length=5)
    post_logout_redirect_uris = models.TextField()
    hash_client_secret = models.IntegerField()
    allowed_origins = models.TextField()

    class Meta:
        managed = False
        db_table = 'oauth2_provider_application'


class Oauth2ProviderGrant(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=255)
    expires = models.DateTimeField()
    redirect_uri = models.TextField()
    scope = models.TextField()
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    code_challenge = models.CharField(max_length=128)
    code_challenge_method = models.CharField(max_length=10)
    nonce = models.CharField(max_length=255)
    claims = models.TextField()

    class Meta:
        managed = False
        db_table = 'oauth2_provider_grant'


class Oauth2ProviderIdtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    jti = models.CharField(unique=True, max_length=32)
    expires = models.DateTimeField()
    scope = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_idtoken'


class Oauth2ProviderRefreshtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(max_length=255)
    access_token = models.OneToOneField(Oauth2ProviderAccesstoken, models.DO_NOTHING, blank=True, null=True)
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    revoked = models.DateTimeField(blank=True, null=True)
    token_family = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_refreshtoken'
        unique_together = (('token', 'revoked'),)


class SocialAuthAssociation(models.Model):
    id = models.BigAutoField(primary_key=True)
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'social_auth_association'
        unique_together = (('server_url', 'handle'),)


class SocialAuthCode(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=254)
    code = models.CharField(max_length=32)
    verified = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_code'
        unique_together = (('email', 'code'),)


class SocialAuthNonce(models.Model):
    id = models.BigAutoField(primary_key=True)
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=65)

    class Meta:
        managed = False
        db_table = 'social_auth_nonce'
        unique_together = (('server_url', 'timestamp', 'salt'),)


class SocialAuthPartial(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(max_length=32)
    next_step = models.PositiveSmallIntegerField()
    backend = models.CharField(max_length=32)
    timestamp = models.DateTimeField()
    data = models.JSONField()

    class Meta:
        managed = False
        db_table = 'social_auth_partial'


class SocialAuthUsersocialauth(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    extra_data = models.JSONField()

    class Meta:
        managed = False
        db_table = 'social_auth_usersocialauth'
        unique_together = (('provider', 'uid'),)


class TokenBlacklistBlacklistedtoken(models.Model):
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    user_id = models.BigIntegerField(blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(unique=True, max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    family_name = models.CharField(max_length=255, blank=True, null=True)
    given_name = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    picture = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class UsersGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_groups'
        unique_together = (('user', 'group'),)


class UsersUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_user_permissions'
        unique_together = (('user', 'permission'),)
