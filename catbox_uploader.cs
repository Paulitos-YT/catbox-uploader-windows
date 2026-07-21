using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace CatboxUploader
{
    static class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            // Enable TLS 1.2 (Required for modern HTTPS APIs like Catbox.moe)
            System.Net.ServicePointManager.SecurityProtocol = (System.Net.SecurityProtocolType)3072; // TLS 1.2

            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            if (args.Length == 0)
            {
                MessageBox.Show("No file selected!\nPlease use the Windows Context Menu (Right-Click) integration to upload files.", 
                    "Catbox Uploader", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            string filePath = args[0];
            if (!File.Exists(filePath))
            {
                MessageBox.Show(string.Format("File not found:\n{0}", filePath), 
                    "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Create a simple form to show progress
            Form progressForm = new Form
            {
                Text = "Catbox Uploader",
                Size = new System.Drawing.Size(350, 120),
                FormBorderStyle = FormBorderStyle.FixedDialog,
                StartPosition = FormStartPosition.CenterScreen,
                MaximizeBox = false,
                MinimizeBox = false
            };

            Label lblStatus = new Label
            {
                Text = "Uploading file: " + Path.GetFileName(filePath),
                AutoSize = true,
                Location = new System.Drawing.Point(20, 20)
            };
            
            ProgressBar progressBar = new ProgressBar
            {
                Style = ProgressBarStyle.Marquee,
                Location = new System.Drawing.Point(20, 45),
                Size = new System.Drawing.Size(290, 20)
            };

            progressForm.Controls.Add(lblStatus);
            progressForm.Controls.Add(progressBar);

            progressForm.Shown += async (s, e) =>
            {
                await UploadFileAsync(filePath, progressForm);
            };

            Application.Run(progressForm);
        }

        static async Task UploadFileAsync(string filePath, Form form)
        {
            try
            {
                using (HttpClient client = new HttpClient())
                {
                    client.DefaultRequestHeaders.UserAgent.ParseAdd("Mozilla/5.0 (Windows NT 10.0; Win64; x64)");

                    using (var content = new MultipartFormDataContent())
                    {
                        content.Add(new StringContent("fileupload"), "reqtype");

                        byte[] fileBytes = File.ReadAllBytes(filePath);
                        var fileContent = new ByteArrayContent(fileBytes);
                        fileContent.Headers.ContentType = MediaTypeHeaderValue.Parse("application/octet-stream");
                        
                        content.Add(fileContent, "fileToUpload", Path.GetFileName(filePath));

                        HttpResponseMessage response = await client.PostAsync("https://catbox.moe/user/api.php", content);
                        string responseString = await response.Content.ReadAsStringAsync();

                        if (response.IsSuccessStatusCode && responseString.StartsWith("http"))
                        {
                            Clipboard.SetText(responseString);
                            form.Hide();
                            MessageBox.Show(string.Format("Upload completed successfully!\n\nLink (Copied to clipboard):\n{0}", responseString), 
                                "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        }
                        else
                        {
                            form.Hide();
                            MessageBox.Show(string.Format("Upload failed!\nServer response:\n{0}", responseString), 
                                "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                form.Hide();
                string errorMsg = string.Format("An error occurred during upload:\n{0}", ex.Message);
                if (ex.InnerException != null)
                {
                    errorMsg += string.Format("\n\nDetails:\n{0}", ex.InnerException.Message);
                }
                MessageBox.Show(errorMsg, 
                    "Critical Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
                form.Close();
            }
        }
    }
}
