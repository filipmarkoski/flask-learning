IF NOT EXISTS (SELECT * FROM sys.tables WHERE Name = 'Todos' and SCHEMA_NAME(schema_id) = 'dbo')
CREATE TABLE dbo.Todos (
    [ID] [BIGINT] IDENTITY(1,1) NOT NULL,
    [Name] [NVARCHAR](128) NOT NULL,
    [Description] [NVARCHAR](MAX) NULL,
    [DateCreated] [DATETIME] NOT NULL DEFAULT GETUTCDATE(),
    [DateModified] [DATETIME] NULL,
    [IsActive] [BIT] NOT NULL,
    [UUID] [UNIQUEIDENTIFIER] NOT NULL DEFAULT NEWID(),
CONSTRAINT [PK_Todos] PRIMARY KEY CLUSTERED 
(ID ASC))
GO

INSERT INTO dbo.Todos (Name, Description, IsActive)
VALUES 
('Learn React', 'Learn React Description', 1),
('Learn Redux', 'Learn Redux Description', 1),
('Learn Material', 'Learn Material Description', 1),
('Learn Native', 'Learn Native Description', 1)